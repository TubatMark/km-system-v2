from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.db.models import Q, Count
from datetime import datetime, timedelta
from utils.get_models import get_active_models
import json
import re

from appAdmin.models import (
    ResourceMetadata,
    Event,
    InformationSystem,
    Map,
    Media,
    News,
    Policy,
    Project,
    Publication,
    Technology,
    TrainingSeminar,
    Webinar,
    Product,
    Tag,
    Commodity,
    KnowledgeResources,
)
from appAdmin.forms import (
    ResourceMetadataForm,
    EventForm,
    InformationSystemForm,
    MapForm,
    MediaForm,
    NewsForm,
    PolicyForm,
    ProjectForm,
    PublicationForm,
    TechnologyForm,
    TrainingSeminarForm,
    WebinarForm,
    ProductForm,
    CommoditySelectForm,
    TagForm,
)
from utils.user_control import user_access_required


@user_access_required("admin")
@user_access_required("admin")
def admin_resources_post(request):
    """
    Enhanced view function to display all resource posts with advanced filtering options.
    """

    models = get_active_models()  # Fetch active models
    commodities = models.get("commodities", [])  # List of active commodities
    knowledge_resources = models.get("knowledge_resources", [])

    # Enhanced filter parameter extraction
    resource_types = request.GET.getlist("resource_types")  # Multiple resource types
    commodity_ids = request.GET.getlist("commodity")  # Multiple commodities
    tag_ids = request.GET.getlist("tags")  # Multiple tags
    status_filters = request.GET.getlist("status")  # Multiple status filters
    date_filter = request.GET.get("date_filter", "year")  # Date range filter
    search_query = request.GET.get("search", "").strip()

    # Legacy single-value filters for backward compatibility
    single_resource_type = request.GET.get("resource_type", "")
    single_commodity_id = request.GET.get("commodity", "")
    single_tag_id = request.GET.get("tag", "")
    single_approval_status = request.GET.get("approval_status", "")

    # Merge single and multiple filters for backward compatibility
    if single_resource_type and single_resource_type not in resource_types:
        resource_types.append(single_resource_type)
    if single_commodity_id and single_commodity_id not in commodity_ids:
        commodity_ids.append(single_commodity_id)
    if single_tag_id and single_tag_id not in tag_ids:
        tag_ids.append(single_tag_id)
    if single_approval_status and single_approval_status not in status_filters:
        status_filters.append(single_approval_status)

    # Calculate totals for dashboard stats
    total_resources = ResourceMetadata.objects.all().count()
    total_approved_resources = ResourceMetadata.objects.filter(is_approved=True).count()
    total_pending_resources = ResourceMetadata.objects.filter(is_approved=False).count()

    # Start with optimized base queryset
    resources = (
        ResourceMetadata.objects.select_related("created_by")
        .prefetch_related("tags", "commodities")
        .order_by("-created_at")
    )

    # Apply resource type filtering
    if resource_types:
        # Handle both slug-based and ID-based filtering
        kr_filters = []
        for rt in resource_types:
            # Try to find knowledge resource by slug
            for kr in knowledge_resources:
                if kr.slug == rt:
                    kr_filters.append(f"KnowledgeResources object ({kr.knowledge_id})")
                    break
            else:
                # If not found as slug, treat as direct resource type
                kr_filters.append(rt)

        if kr_filters:
            resources = resources.filter(resource_type__in=kr_filters)

    # Apply commodity filtering
    if commodity_ids:
        commodity_q = Q()
        for commodity_id in commodity_ids:
            try:
                # Handle both ID and slug-based filtering
                if commodity_id.isdigit():
                    commodity_q |= Q(commodities__id=int(commodity_id))
                else:
                    commodity_q |= Q(commodities__slug=commodity_id)
            except (ValueError, AttributeError):
                continue

        if commodity_q:
            resources = resources.filter(commodity_q).distinct()

    # Apply tag filtering
    if tag_ids:
        tag_q = Q()
        for tag_id in tag_ids:
            try:
                # Handle both ID and slug-based filtering
                if tag_id.isdigit():
                    tag_q |= Q(tags__id=int(tag_id))
                else:
                    tag_q |= Q(tags__slug=tag_id)
            except (ValueError, AttributeError):
                continue

        if tag_q:
            resources = resources.filter(tag_q).distinct()

    # Apply status filtering
    if status_filters:
        status_q = Q()

        if "approved" in status_filters:
            status_q |= Q(is_approved=True)
        if "pending" in status_filters:
            status_q |= Q(is_approved=False)
        if "featured" in status_filters:
            status_q |= Q(is_featured=True)

        if status_q:
            resources = resources.filter(status_q)

    # Apply date filtering
    if date_filter and date_filter != "all":
        now = datetime.now()

        if date_filter == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            resources = resources.filter(created_at__gte=start_date)
        elif date_filter == "week":
            start_date = now - timedelta(days=7)
            resources = resources.filter(created_at__gte=start_date)
        elif date_filter == "month":
            start_date = now - timedelta(days=30)
            resources = resources.filter(created_at__gte=start_date)
        elif date_filter == "year":
            start_date = now - timedelta(days=365)
            resources = resources.filter(created_at__gte=start_date)

    # Apply search filtering
    if search_query:
        search_q = Q()

        # Search in multiple fields
        search_fields = [
            "title__icontains",
            "description__icontains",
            "keywords__icontains",
            "tags__name__icontains",
            "created_by__first_name__icontains",
            "created_by__last_name__icontains",
        ]

        for field in search_fields:
            search_q |= Q(**{field: search_query})

        resources = resources.filter(search_q).distinct()

    # 🔥 GET ACTUAL RESOURCE COUNTS FROM INDIVIDUAL MODELS
    def get_resource_counts_by_knowledge_resource():
        """
        Get counts for each resource type from their individual models
        """
        resource_counts = {}

        # Helper function to get count with metadata relationship
        def get_model_count(model_class, knowledge_resource_id):
            try:
                kr_string = f"KnowledgeResources object ({knowledge_resource_id})"
                return model_class.objects.filter(
                    metadata__resource_type=kr_string
                ).count()
            except:
                return 0

        # Map each knowledge resource to its corresponding model
        resource_model_mapping = {
            "events": Event,
            "information_systemswebsites": InformationSystem,
            "maps": Map,
            "media": Media,
            "news": News,
            "policies": Policy,
            "projects": Project,
            "publications": Publication,
            "technologies": Technology,
            "trainingseminars": TrainingSeminar,
            "webinars": Webinar,
            "products": Product,
        }

        for kr in knowledge_resources:
            machine_name = kr.machine_name
            model_class = resource_model_mapping.get(machine_name)

            if model_class:
                try:
                    # Get count from the specific model
                    count = model_class.objects.count()
                    resource_counts[kr.slug] = count
                except:
                    resource_counts[kr.slug] = 0
            else:
                resource_counts[kr.slug] = 0

        return resource_counts

    # Get the actual resource counts
    resource_counts = get_resource_counts_by_knowledge_resource()

    # Add resource counts to knowledge_resources for template display
    for kr in knowledge_resources:
        kr.resource_count = resource_counts.get(kr.slug, 0)

    # Pagination
    paginator = Paginator(resources, 10)  # Show 10 resources per page
    page = request.GET.get("page")

    try:
        resources_page = paginator.page(page)
    except PageNotAnInteger:
        resources_page = paginator.page(1)
    except EmptyPage:
        resources_page = paginator.page(paginator.num_pages)

    # Get additional data for filters
    resource_types_choices = (
        ResourceMetadata.RESOURCE_TYPES
        if hasattr(ResourceMetadata, "RESOURCE_TYPES")
        else []
    )
    all_commodities = Commodity.objects.all()

    # Get common tags with usage counts
    common_tags = (
        Tag.objects.annotate(resource_count=Count("resourcemetadata"))
        .filter(resource_count__gt=0)
        .order_by("-resource_count")[:15]
    )

    # Initialize forms for the modal (existing code)
    metadata_form = ResourceMetadataForm()
    event_form = EventForm()
    information_system_form = InformationSystemForm()
    map_form = MapForm()
    media_form = MediaForm()
    news_form = NewsForm()
    policy_form = PolicyForm()
    project_form = ProjectForm()
    publication_form = PublicationForm()
    technology_form = TechnologyForm()
    training_seminar_form = TrainingSeminarForm()
    webinar_form = WebinarForm()
    product_form = ProductForm()

    # Enhanced context with all filtering data
    context = {
        # Core data
        "knowledge_resources": knowledge_resources,  # Now includes resource_count
        "resources": resources_page,
        "resources_data": resources_page,  # For backward compatibility
        # Filter options
        "resource_types": resource_types_choices,
        "commodities": all_commodities,
        "tags": Tag.objects.all(),
        "common_tags": common_tags,
        # Resource counts
        "resource_counts": resource_counts,
        # Current filter state
        "current_filters": {
            "resource_types": resource_types,
            "resource_type": single_resource_type,  # Backward compatibility
            "commodity": commodity_ids,
            "tags": tag_ids,
            "tag": single_tag_id,  # Backward compatibility
            "status": status_filters,
            "approval_status": single_approval_status,  # Backward compatibility
            "date_filter": date_filter,
            "search": search_query,
        },
        # Statistics
        "total_resources": total_resources,
        "total_approved_resources": total_approved_resources,
        "total_pending_resources": total_pending_resources,
        # Forms (existing)
        "metadata_form": metadata_form,
        "event_form": event_form,
        "information_system_form": information_system_form,
        "map_form": map_form,
        "media_form": media_form,
        "news_form": news_form,
        "policy_form": policy_form,
        "project_form": project_form,
        "publication_form": publication_form,
        "technology_form": technology_form,
        "training_seminar_form": training_seminar_form,
        "webinar_form": webinar_form,
        "product_form": product_form,
    }

    return render(request, "pages/resources-post.html", context)


@user_access_required("admin")
@transaction.atomic
def admin_add_resources_post(request):
    """
    View for handling resource creation from the admin panel.
    """
    # Use the get_active_models utility to fetch required data
    models = get_active_models()
    commodities = models.get("commodities", [])
    knowledge_resources = models.get("knowledge_resources", [])

    # For GET requests, just render the form
    if request.method == "GET":
        context = {
            "commodities": commodities,
            "knowledge_resources": knowledge_resources,
        }
        return render(request, "pages/resources-post.html", context)

    # For POST requests, process the form data
    elif request.method == "POST":
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        is_draft = request.POST.get("isDraft") == "true"

        try:
            # Get common metadata from the form
            resource_type_slug = request.POST.get("resourceType")
            resource_title = request.POST.get("resourceTitle")
            resource_description = request.POST.get("resourceDescription")
            is_approved = "is_approved" in request.POST

            # Find the actual resource type using the slug
            resource_type = None
            resource_machine_name = None
            for kr in knowledge_resources:
                if kr.slug == resource_type_slug:
                    resource_type = kr
                    # Extract the machine name from the data-fields-id attribute
                    # This should match with one of the resource type handlers
                    resource_machine_name = kr.machine_name
                    break

            if not resource_type:
                raise ValueError(
                    f"Resource type with slug '{resource_type_slug}' not found"
                )

            # Create resource metadata
            metadata = ResourceMetadata.objects.create(
                resource_type=resource_type,
                is_approved=is_approved,
                created_by=request.user,
            )

            # Process tags
            tags_string = request.POST.get("tags", "")
            if tags_string:
                tag_names = [tag.strip() for tag in tags_string.split(",")]
                for tag_name in tag_names:
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        metadata.tags.add(tag)

            # Process commodities
            commodity_ids = request.POST.get("commodity_ids", "")
            if commodity_ids:
                commodity_slugs = commodity_ids.split(",")
                for slug in commodity_slugs:
                    try:
                        commodity = Commodity.objects.get(slug=slug)
                        metadata.commodities.add(commodity)
                    except Commodity.DoesNotExist:
                        pass

            # Handle specific resource type fields
            if resource_machine_name:
                create_resource_specific_data(request, resource_machine_name, metadata)

            # Successful response
            if is_ajax:
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Resource created successfully!",
                        "redirect": f"appAdmin:display-resources-post",
                    }
                )
            else:
                messages.success(request, "Resource created successfully!")
                return redirect("appAdmin:display-resources-post")

        except Exception as e:
            # Handle errors
            if is_ajax:
                return JsonResponse(
                    {"success": False, "message": f"Error creating resource: {str(e)}"}
                )
            else:
                messages.error(request, f"Error creating resource: {str(e)}")
                context = {
                    "commodities": commodities,
                    "knowledge_resources": knowledge_resources,
                    "form_data": request.POST,
                    "error": str(e),  # Send the error to the template for debugging
                }
                return render(request, "pages/resources-post.html", context)

    # For other request methods
    return JsonResponse(
        {"success": False, "message": "Invalid request method"}, status=405
    )


@user_access_required("admin")
def create_resource_specific_data(request, resource_machine_name, metadata):
    """
    Helper function to create specific resource data based on machine name.
    """
    # Maps machine names to model handlers
    resource_handlers = {
        "events": create_event,
        "information_systemswebsites": create_information_system,
        "maps": create_map,
        "media": create_media,
        "news": create_news,
        "policies": create_policy,
        "projects": create_project,
        "publications": create_publication,
        "technologies": create_technology,
        "trainingseminars": create_training_seminar,
        "webinars": create_webinar,
        "products": create_product,
    }

    # Find and call the appropriate handler
    handler = resource_handlers.get(resource_machine_name)
    if handler:
        handler(request, metadata)
    else:
        raise ValueError(f"Unknown resource type: {resource_machine_name}")


# The following functions handle specific resource types


@user_access_required("admin")
def create_event(request, metadata):
    Event.objects.create(
        metadata=metadata,
        title=request.POST.get("eventTitle"),
        venue=request.POST.get("eventVenue"),
        organizer=request.POST.get("eventOrganizer"),
        start_date=request.POST.get("eventStartDate"),
        end_date=request.POST.get("eventEndDate"),
        event_type=request.POST.get("eventType"),
        documentation_link=request.POST.get("eventDocumentationLink"),
        pictures=request.FILES.get("eventPictures"),
    )


@user_access_required("admin")
def create_information_system(request, metadata):
    InformationSystem.objects.create(
        metadata=metadata,
        link=request.POST.get("infoSystemLink"),
        organization_owner=request.POST.get("infoSystemOwner"),
        agency=request.POST.get("infoSystemAgency"),
        brief_explanation=request.POST.get("infoSystemBriefExplanation"),
    )


@user_access_required("admin")
def create_map(request, metadata):
    Map.objects.create(
        metadata=metadata,
        map_file=request.FILES.get("mapFile"),
        map_url=request.POST.get("mapUrl"),
        latitude=request.POST.get("mapLatitude") or None,
        longitude=request.POST.get("mapLongitude") or None,
    )


@user_access_required("admin")
def create_media(request, metadata):
    Media.objects.create(
        metadata=metadata,
        title=request.POST.get("mediaTitle"),
        link=request.POST.get("mediaLink"),
    )


@user_access_required("admin")
def create_news(request, metadata):
    News.objects.create(
        metadata=metadata,
        headline=request.POST.get("newsHeadline"),
        author=request.POST.get("newsAuthor"),
        position=request.POST.get("newsPosition"),
        content=request.POST.get("newsContent"),
        source=request.POST.get("newsSource"),
        featured_image=request.FILES.get("newsFeaturedImage"),
    )


@user_access_required("admin")
def create_policy(request, metadata):
    Policy.objects.create(
        metadata=metadata,
        policy_type=request.POST.get("policyType"),
        advocacy_project=request.POST.get("policyAdvocacyProject"),
        agency=request.POST.get("policyAgency"),
        author=request.POST.get("policyAuthor"),
        description=request.POST.get("policyDescription"),
        findings=request.POST.get("policyFindings"),
        year=request.POST.get("policyYear"),
        policy=request.POST.get("policy"),
    )


@user_access_required("admin")
def create_project(request, metadata):
    Project.objects.create(
        metadata=metadata,
        program_title=request.POST.get("projectProgramTitle"),
        project_title=request.POST.get("projectTitle"),
        project_leader=request.POST.get("projectLeader"),
        source_of_fund=request.POST.get("projectSourceOfFund"),
        cooperating_agency=request.POST.get("projectCooperatingAgency"),
        collaborating_agency=request.POST.get("projectCollaboratingAgency"),
        implementing_agency=request.POST.get("projectImplementingAgency"),
        total_approved_budget=request.POST.get("projectTotalApprovedBudget") or None,
        implementing_agency_counterpart=request.POST.get(
            "projectImplementingAgencyCounterpart"
        )
        or None,
        start_date=request.POST.get("projectStartDate"),
        end_date=request.POST.get("projectEndDate") or None,
        extension_months=request.POST.get("projectExtensionMonths") or None,
        contact_email=request.POST.get("projectContactEmail"),
        status=request.POST.get("projectStatus"),
    )


@user_access_required("admin")
def create_publication(request, metadata):
    Publication.objects.create(
        metadata=metadata,
        title=request.POST.get("publicationTitle"),
        description=request.POST.get("publicationDescription"),
        author=request.POST.get("publicationAuthor"),
        file=request.FILES.get("publicationFile"),
        date_published=request.POST.get("publicationDatePublished"),
        publisher=request.POST.get("publicationPublisher"),
        doi=request.POST.get("publicationDOI"),
        isbn=request.POST.get("publicationISBN"),
        publication_type=request.POST.get("publicationType"),
    )


@user_access_required("admin")
def create_technology(request, metadata):
    Technology.objects.create(
        metadata=metadata,
        commodity_id=request.POST.get("technologyCommodityId"),
        technologies=request.POST.get("technologyTechnologies"),
        products=request.POST.get("technologyProducts"),
        adoption_status=request.POST.get("technologyAdoptionStatus"),
        year_introduced=request.POST.get("technologyYearIntroduced"),
        ip_asset=request.POST.get("technologyIpAsset"),
        brief_description=request.POST.get("technologyBriefDescription"),
        support_facilities=request.POST.get("technologySupportFacilities"),
        available_experts=request.POST.get("technologyAvailableExperts"),
        experts_email=request.POST.get("technologyExpertsEmail"),
        experts_phone=request.POST.get("technologyExpertsPhone"),
        funding_source=request.POST.get("technologyFundingSource"),
        technologies_offered_for=request.POST.get("technologyOfferedFor"),
        technology_transfer_pathway=request.POST.get("technologyTransferPathway"),
        google_link_photos=request.POST.get("technologyGoogleLinkPhotos"),
        pictures=request.FILES.get("technologyPictures"),
    )


@user_access_required("admin")
def create_training_seminar(request, metadata):
    TrainingSeminar.objects.create(
        metadata=metadata,
        title=request.POST.get("trainingTitle"),
        description=request.POST.get("trainingDescription"),
        start_date=request.POST.get("trainingStartDate") or None,
        end_date=request.POST.get("trainingEndDate") or None,
        venue=request.POST.get("trainingVenue"),
        organizer=request.POST.get("trainingOrganizer"),
        speakers=request.POST.get("trainingSpeakers"),
        total_participants=request.POST.get("trainingTotalParticipants") or None,
        documentation_link=request.POST.get("trainingDocumentationLink"),
        pictures=request.FILES.get("trainingPictures"),
    )


@user_access_required("admin")
def create_webinar(request, metadata):
    Webinar.objects.create(
        metadata=metadata,
        title=request.POST.get("webinarTitle"),
        duration=request.POST.get("webinarDuration"),
        date=request.POST.get("webinarDate"),
        speaker=request.POST.get("webinarSpeaker"),
        platform=request.POST.get("webinarPlatform"),
        attendance=request.POST.get("webinarAttendance") or None,
        documentation_link=request.POST.get("webinarDocumentationLink"),
        pictures=request.FILES.get("webinarPictures"),
    )


@user_access_required("admin")
def create_product(request, metadata):
    Product.objects.create(
        metadata=metadata,
        products=request.POST.get("productProducts"),
        description=request.POST.get("productDescription"),
        company=request.POST.get("productCompany"),
        price=request.POST.get("productPrice") or None,
        contact_info=request.POST.get("productContactInfo"),
        documentation_link=request.POST.get("productDocumentationLink"),
        pictures=request.FILES.get("productPictures"),
    )


@user_access_required("admin")
def admin_edit_resources_post(request, slug):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get("status")

            resource = ResourceMetadata.objects.get(slug=slug)
            resource.is_approved = new_status == "approved"
            resource.save()

            return JsonResponse({"success": True})
        except ResourceMetadata.DoesNotExist:
            return JsonResponse({"success": False, "error": "Resource not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})


@user_access_required("admin")
def admin_delete_resources_post(request, slug):
    resource_metadata_instance = ResourceMetadata.objects.get(slug=slug)
    resource_metadata_instance.delete()
    success_message = "Deleted successfully!"
    messages.success(request, success_message)
    return redirect("appAdmin:display-resources-post")


def view_resource_modal(request, slug):
    """
    API endpoint to get resource data for the view modal
    """
    try:
        resource = get_object_or_404(ResourceMetadata, slug=slug)

        # Prepare base data
        resource_data = {
            "slug": resource.slug,
            "resource_type": resource.resource_type,
            "resource_type_display": dict(ResourceMetadata.RESOURCE_TYPES).get(
                resource.resource_type
            ),
            "keywords": resource.keywords,
            "created_at": resource.created_at.isoformat(),
            "updated_at": (
                resource.updated_at.isoformat() if resource.updated_at else None
            ),
            "is_approved": resource.is_approved,
            "is_featured": getattr(resource, "is_featured", False),
            "created_by": (
                resource.created_by.get_full_name() if resource.created_by else None
            ),
            "tags": [
                {"name": tag.name, "slug": tag.slug} for tag in resource.tags.all()
            ],
            "commodities": [
                {"commodity_name": c.commodity_name, "slug": c.slug}
                for c in resource.commodities.all()
            ],
        }

        # Get the proper knowledge title using the same logic as get_knowledge_title filter
        try:
            if (
                isinstance(resource.resource_type, str)
                and "(" in resource.resource_type
                and ")" in resource.resource_type
            ):
                obj_id = int(str(resource.resource_type).split("(")[1].split(")")[0])
                knowledge_resource = KnowledgeResources.objects.get(knowledge_id=obj_id)
                resource_data["resource_type_display"] = (
                    knowledge_resource.knowledge_title
                )
        except (AttributeError, ValueError, KnowledgeResources.DoesNotExist):
            pass

        # Set title, description, and resource-specific data based on type using metadata relationship
        rt, knowledge_title = extract_machine_name_and_title(resource.resource_type)
        if knowledge_title:
            resource_data["resource_type_display"] = knowledge_title

        # Add the machine name for frontend matching
        resource_data["resource_type_machine_name"] = rt

        if rt == "events":
            try:
                event = resource.event
                resource_data["title"] = event.title
                resource_data["description"] = (
                    f"Event organized by {event.organizer} at {event.venue}"
                )
                resource_data["event_data"] = {
                    "title": event.title,
                    "venue": event.venue,
                    "organizer": event.organizer,
                    "start_date": event.start_date.isoformat(),
                    "end_date": event.end_date.isoformat(),
                    "event_type": event.event_type,
                    "documentation_link": event.documentation_link,
                    "pictures": event.pictures.url if event.pictures else None,
                }
            except Event.DoesNotExist:
                resource_data["title"] = "Event Not Found"
                resource_data["description"] = "Event data not available"

        elif rt == "webinars":
            try:
                webinar = resource.webinar
                resource_data["title"] = webinar.title
                resource_data["description"] = (
                    f"Webinar by {webinar.speaker} on {webinar.platform}"
                )
                resource_data["webinar_data"] = {
                    "title": webinar.title,
                    "duration": webinar.duration,
                    "date": webinar.date.isoformat(),
                    "speaker": webinar.speaker,
                    "platform": webinar.platform,
                    "attendance": webinar.attendance,
                    "documentation_link": webinar.documentation_link,
                    "pictures": webinar.pictures.url if webinar.pictures else None,
                }
            except Webinar.DoesNotExist:
                resource_data["title"] = "Webinar Not Found"
                resource_data["description"] = "Webinar data not available"

        elif rt == "news":
            try:
                news = resource.news
                resource_data["title"] = news.headline
                resource_data["description"] = (
                    news.content[:200] + "..."
                    if len(news.content) > 200
                    else news.content
                )
                resource_data["news_data"] = {
                    "headline": news.headline,
                    "author": news.author,
                    "position": news.position,
                    "content": news.content,
                    "source": news.source,
                    "featured_image": (
                        news.featured_image.url if news.featured_image else None
                    ),
                }
            except News.DoesNotExist:
                resource_data["title"] = "News Not Found"
                resource_data["description"] = "News data not available"

        elif rt == "publications":
            try:
                pub = resource.publication
                resource_data["title"] = pub.title
                resource_data["description"] = pub.description
                resource_data["publication_data"] = {
                    "title": pub.title,
                    "description": pub.description,
                    "author": pub.author,
                    "file": pub.file.url if pub.file else None,
                    "date_published": pub.date_published.isoformat(),
                    "publisher": pub.publisher,
                    "doi": pub.doi,
                    "isbn": pub.isbn,
                    "publication_type": pub.publication_type,
                    "publication_type_display": dict(
                        pub._meta.get_field("publication_type").choices
                    ).get(pub.publication_type),
                }
            except Publication.DoesNotExist:
                resource_data["title"] = "Publication Not Found"
                resource_data["description"] = "Publication data not available"

        elif rt == "technologies":
            try:
                tech = resource.technology
                resource_data["title"] = tech.technologies
                resource_data["description"] = tech.brief_description
                resource_data["technology_data"] = {
                    "technologies": tech.technologies,
                    "products": tech.products,
                    "adoption_status": tech.adoption_status,
                    "adoption_status_display": dict(
                        tech._meta.get_field("adoption_status").choices
                    ).get(tech.adoption_status),
                    "year_introduced": tech.year_introduced,
                    "ip_asset": tech.ip_asset,
                    "brief_description": tech.brief_description,
                    "support_facilities": tech.support_facilities,
                    "available_experts": tech.available_experts,
                    "experts_email": tech.experts_email,
                    "experts_phone": tech.experts_phone,
                    "funding_source": tech.funding_source,
                    "funding_source_display": (
                        dict(tech._meta.get_field("funding_source").choices).get(
                            tech.funding_source
                        )
                        if tech.funding_source
                        else None
                    ),
                    "technologies_offered_for": tech.technologies_offered_for,
                    "technology_transfer_pathway": tech.technology_transfer_pathway,
                    "google_link_photos": tech.google_link_photos,
                    "pictures": tech.pictures.url if tech.pictures else None,
                }
            except Technology.DoesNotExist:
                resource_data["title"] = "Technology Not Found"
                resource_data["description"] = "Technology data not available"

        elif rt == "projects":
            try:
                project = resource.project
                resource_data["title"] = project.project_title
                resource_data["description"] = (
                    f"Project led by {project.project_leader}"
                )
                resource_data["project_data"] = {
                    "program_title": project.program_title,
                    "project_title": project.project_title,
                    "project_leader": project.project_leader,
                    "source_of_fund": project.source_of_fund,
                    "cooperating_agency": project.cooperating_agency,
                    "collaborating_agency": project.collaborating_agency,
                    "implementing_agency": project.implementing_agency,
                    "total_approved_budget": (
                        str(project.total_approved_budget)
                        if project.total_approved_budget
                        else None
                    ),
                    "implementing_agency_counterpart": (
                        str(project.implementing_agency_counterpart)
                        if project.implementing_agency_counterpart
                        else None
                    ),
                    "start_date": project.start_date.isoformat(),
                    "end_date": (
                        project.end_date.isoformat() if project.end_date else None
                    ),
                    "extension_months": project.extension_months,
                    "contact_email": project.contact_email,
                    "status": project.status,
                    "status_display": dict(
                        project._meta.get_field("status").choices
                    ).get(project.status),
                }
            except Project.DoesNotExist:
                resource_data["title"] = "Project Not Found"
                resource_data["description"] = "Project data not available"

        elif rt == "policies":
            try:
                policy = resource.policy
                resource_data["title"] = f"Policy by {policy.agency} ({policy.year})"
                resource_data["description"] = policy.description
                resource_data["policy_data"] = {
                    "policy_type": policy.policy_type,
                    "policy_type_display": dict(
                        policy._meta.get_field("policy_type").choices
                    ).get(policy.policy_type),
                    "advocacy_project": policy.advocacy_project,
                    "agency": policy.agency,
                    "author": policy.author,
                    "description": policy.description,
                    "findings": policy.findings,
                    "year": policy.year,
                    "policy_text": policy.policy,  # Using policy_text as expected in frontend
                }
            except Policy.DoesNotExist:
                resource_data["title"] = "Policy Not Found"
                resource_data["description"] = "Policy data not available"

        elif rt == "trainingseminars":
            try:
                training = resource.training_seminar
                resource_data["title"] = training.title
                resource_data["description"] = training.description
                resource_data["training_data"] = {
                    "title": training.title,
                    "description": training.description,
                    "start_date": (
                        training.start_date.isoformat() if training.start_date else None
                    ),
                    "end_date": (
                        training.end_date.isoformat() if training.end_date else None
                    ),
                    "venue": training.venue,
                    "organizer": training.organizer,
                    "speakers": training.speakers,
                    "total_participants": training.total_participants,
                    "documentation_link": training.documentation_link,
                    "pictures": training.pictures.url if training.pictures else None,
                }
            except TrainingSeminar.DoesNotExist:
                resource_data["title"] = "Training Not Found"
                resource_data["description"] = "Training data not available"

        elif rt == "media":
            try:
                media = resource.media
                resource_data["title"] = media.title
                resource_data["description"] = f"Media resource: {media.title}"
                resource_data["media_data"] = {
                    "title": media.title,
                    "link": media.link,
                }
            except Media.DoesNotExist:
                resource_data["title"] = "Media Not Found"
                resource_data["description"] = "Media data not available"

        elif rt == "products":
            try:
                product = resource.product
                resource_data["title"] = product.products
                resource_data["description"] = product.description
                resource_data["product_data"] = {
                    "products": product.products,
                    "description": product.description,
                    "company": product.company,
                    "price": str(product.price) if product.price else None,
                    "contact_info": product.contact_info,
                    "documentation_link": product.documentation_link,
                    "pictures": product.pictures.url if product.pictures else None,
                }
            except Product.DoesNotExist:
                resource_data["title"] = "Product Not Found"
                resource_data["description"] = "Product data not available"

        elif rt == "information_systemswebsites":
            try:
                info_sys = resource.information_system
                resource_data["title"] = (
                    f"Information System by {info_sys.organization_owner}"
                )
                resource_data["description"] = info_sys.brief_explanation
                resource_data["info_system_data"] = {
                    "link": info_sys.link,
                    "organization_owner": info_sys.organization_owner,
                    "agency": info_sys.agency,
                    "brief_explanation": info_sys.brief_explanation,
                }
            except InformationSystem.DoesNotExist:
                resource_data["title"] = "Information System Not Found"
                resource_data["description"] = "Information System data not available"

        elif rt == "maps":
            try:
                map_resource = resource.map
                resource_data["title"] = "Map Resource"
                resource_data["description"] = "Geographic information and mapping data"
                resource_data["map_data"] = {
                    "map_file": (
                        map_resource.map_file.url if map_resource.map_file else None
                    ),
                    "map_url": map_resource.map_url,
                    "latitude": (
                        str(map_resource.latitude) if map_resource.latitude else None
                    ),
                    "longitude": (
                        str(map_resource.longitude) if map_resource.longitude else None
                    ),
                }
            except Map.DoesNotExist:
                resource_data["title"] = "Map Not Found"
                resource_data["description"] = "Map data not available"
        else:
            resource_data["title"] = "Unknown Resource Type"
            resource_data["description"] = "Resource type not recognized"

        return JsonResponse(resource_data)

    except Exception as e:
        import traceback

        return JsonResponse(
            {"error": "Failed to load resource details", "message": str(e)}, status=500
        )


def extract_machine_name_and_title(resource_type):
    # If resource_type is like "KnowledgeResources object (23)", extract the ID and get the machine_name and knowledge_title
    if isinstance(resource_type, str) and "KnowledgeResources object" in resource_type:
        match = re.search(r"\((\d+)\)", resource_type)
        if match:
            obj_id = int(match.group(1))
            try:
                knowledge_resource = KnowledgeResources.objects.get(knowledge_id=obj_id)
                return (
                    knowledge_resource.machine_name,
                    knowledge_resource.knowledge_title,
                )
            except KnowledgeResources.DoesNotExist:
                return None, None
    return resource_type, None  # Already normalized
