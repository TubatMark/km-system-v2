from .models import (
    Commodity,
    KnowledgeResources,
    About,
    AboutFooter,
    CMI,
    UploadVideo,
    UsefulLinks,
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
)
from django import forms


class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CommodityForm, self).__init__(*args, **kwargs)
        self.fields["date_created"].required = False
        self.fields["commodity_img"].required = False
        self.fields["status"].required = False


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = "__all__"


class AboutFooterForm(forms.ModelForm):
    class Meta:
        model = AboutFooter
        fields = "__all__"


class KnowledgeForm(forms.ModelForm):
    class Meta:
        model = KnowledgeResources
        fields = ["knowledge_title", "knowledge_description"]


class CMIForm(forms.ModelForm):
    class Meta:
        model = CMI
        fields = [
            "cmi_name",
            "cmi_meaning",
            "cmi_description",
            "address",
            "contact_num",
            "email",
            "latitude",
            "longitude",
            "cmi_image",
            "url",
            "date_joined",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Making some fields optional
        for field in [
            "cmi_name",
            "cmi_meaning",
            "cmi_description",
            "address",
            "contact_num",
            "email",
            "latitude",
            "longitude",
            "url",
            "date_joined",
        ]:
            self.fields[field].required = False


class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadVideo
        fields = "__all__"


class UsefulLinksForm(forms.ModelForm):
    class Meta:
        model = UsefulLinks
        fields = [
            "link_title",
            "link",
        ]

    def __init__(self, *args, **kwargs):
        super(UsefulLinksForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False


class ResourceMetadataForm(forms.ModelForm):
    """Form for the common metadata fields for all resource types."""

    class Meta:
        model = ResourceMetadata
        fields = ["resource_type", "keywords", "is_approved"]
        widgets = {
            "resource_type": forms.Select(
                attrs={"class": "form-select", "onchange": "showResourceFields()"}
            ),
            "keywords": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter comma-separated keywords for search and categorization",
                }
            ),
            "is_approved": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "venue",
            "organizer",
            "start_date",
            "end_date",
            "event_type",
            "documentation_link",
            "pictures",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event title"}
            ),
            "venue": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event venue"}
            ),
            "organizer": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter organizer name"}
            ),
            "start_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "event_type": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event type"}
            ),
            "documentation_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com/documentation",
                }
            ),
            "pictures": forms.FileInput(attrs={"class": "form-control"}),
        }


class InformationSystemForm(forms.ModelForm):
    class Meta:
        model = InformationSystem
        fields = ["link", "organization_owner", "agency", "brief_explanation"]
        widgets = {
            "link": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://example.com"}
            ),
            "organization_owner": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter organization/owner",
                }
            ),
            "agency": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter agency name"}
            ),
            "brief_explanation": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Provide a brief explanation of the system",
                }
            ),
        }


class MapForm(forms.ModelForm):
    class Meta:
        model = Map
        fields = ["map_file", "map_url", "latitude", "longitude"]
        widgets = {
            "map_file": forms.FileInput(attrs={"class": "form-control"}),
            "map_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com/map",
                }
            ),
            "latitude": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.00000001"}
            ),
            "longitude": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.00000001"}
            ),
        }


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ["title", "link"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter media title"}
            ),
            "link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com/media",
                }
            ),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            "headline",
            "author",
            "position",
            "content",
            "source",
            "featured_image",
        ]
        widgets = {
            "headline": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter news headline"}
            ),
            "author": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter author name"}
            ),
            "position": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter author's position/title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Enter news content",
                }
            ),
            "source": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com/news-source",
                }
            ),
            "featured_image": forms.FileInput(attrs={"class": "form-control"}),
        }


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = [
            "policy_type",
            "advocacy_project",
            "agency",
            "author",
            "description",
            "findings",
            "year",
            "policy",
        ]
        widgets = {
            "policy_type": forms.Select(
                attrs={"class": "form-select", "onchange": "togglePolicyFields()"}
            ),
            "advocacy_project": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter advocacy project name",
                }
            ),
            "agency": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter agency name"}
            ),
            "author": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter author name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Provide policy description",
                }
            ),
            "findings": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter research findings (for policy research)",
                }
            ),
            "year": forms.NumberInput(
                attrs={"class": "form-control", "min": "1900", "max": "2100"}
            ),
            "policy": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter policy",
                }
            ),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "program_title",
            "project_title",
            "project_leader",
            "source_of_fund",
            "cooperating_agency",
            "collaborating_agency",
            "implementing_agency",
            "total_approved_budget",
            "implementing_agency_counterpart",
            "start_date",
            "end_date",
            "extension_months",
            "contact_email",
            "status",
        ]
        widgets = {
            "program_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter program title (optional)",
                }
            ),
            "project_title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter project title"}
            ),
            "project_leader": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter project leader name",
                }
            ),
            "source_of_fund": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter funding source"}
            ),
            "cooperating_agency": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter cooperating agency",
                }
            ),
            "collaborating_agency": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter collaborating agency",
                }
            ),
            "implementing_agency": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter implementing agency",
                }
            ),
            "total_approved_budget": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "implementing_agency_counterpart": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "extension_months": forms.NumberInput(
                attrs={"class": "form-control", "min": "0"}
            ),
            "contact_email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter contact email"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = [
            "title",
            "description",
            "author",
            "file",
            "date_published",
            "publisher",
            "doi",
            "isbn",
            "publication_type",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter publication title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Provide publication description",
                }
            ),
            "author": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter author name(s)",
                }
            ),
            "file": forms.FileInput(attrs={"class": "form-control"}),
            "date_published": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "publisher": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter publisher name"}
            ),
            "doi": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., 10.1000/xyz123"}
            ),
            "isbn": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., 978-3-16-148410-0",
                }
            ),
            "publication_type": forms.Select(attrs={"class": "form-select"}),
        }


class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = [
            "commodity",
            "technologies",
            "products",
            "adoption_status",
            "year_introduced",
            "ip_asset",
            "brief_description",
            "support_facilities",
            "available_experts",
            "experts_email",
            "experts_phone",
            "funding_source",
            "technologies_offered_for",
            "technology_transfer_pathway",
            "google_link_photos",
            "pictures",
        ]
        widgets = {
            "commodity": forms.Select(attrs={"class": "form-select"}),
            "technologies": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter technology name"}
            ),
            "products": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter products"}
            ),
            "adoption_status": forms.Select(attrs={"class": "form-select"}),
            "year_introduced": forms.NumberInput(
                attrs={"class": "form-control", "min": "1900", "max": "2100"}
            ),
            "ip_asset": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter IP asset information",
                }
            ),
            "brief_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Brief description of technology & product",
                }
            ),
            "support_facilities": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter support facilities",
                }
            ),
            "available_experts": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "List available experts",
                }
            ),
            "experts_email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter expert email"}
            ),
            "experts_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter expert phone number",
                }
            ),
            "funding_source": forms.Select(attrs={"class": "form-select"}),
            "technologies_offered_for": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Technologies offered for...",
                }
            ),
            "technology_transfer_pathway": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Describe technology transfer pathway",
                }
            ),
            "google_link_photos": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://photos.google.com/...",
                }
            ),
            "pictures": forms.FileInput(attrs={"class": "form-control"}),
        }


class TrainingSeminarForm(forms.ModelForm):
    class Meta:
        model = TrainingSeminar
        fields = [
            "title",
            "description",
            "start_date",
            "end_date",
            "venue",
            "organizer",
            "speakers",
            "total_participants",
            "documentation_link",
            "pictures",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter training/seminar title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Provide training description",
                }
            ),
            "start_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "venue": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter venue",
                }
            ),
            "venue": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter venue"}
            ),
            "organizer": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter organizer"}
            ),
            "speakers": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "List speakers/trainers",
                }
            ),
            "total_participants": forms.NumberInput(
                attrs={"class": "form-control", "min": "0"}
            ),
            "documentation_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com/documentation",
                }
            ),
            "pictures": forms.FileInput(attrs={"class": "form-control"}),
        }


class WebinarForm(forms.ModelForm):
    class Meta:
        model = Webinar
        fields = [
            "title",
            "duration",
            "date",
            "speaker",
            "platform",
            "attendance",
            "documentation_link",
            "pictures",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter webinar title"}
            ),
            "duration": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Duration in minutes",
                }
            ),
            "date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "speaker": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter speaker name"}
            ),
            "platform": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Zoom, Teams, etc.",
                }
            ),
            "attendance": forms.NumberInput(
                attrs={"class": "form-control", "min": "0"}
            ),
            "documentation_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com/documentation",
                }
            ),
            "pictures": forms.FileInput(attrs={"class": "form-control"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "products",
            "description",
            "company",
            "price",
            "contact_info",
            "documentation_link",
            "pictures",
        ]
        widgets = {
            "products": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter product name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Provide product description",
                }
            ),
            "company": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter company name"}
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Price in PHP",
                }
            ),
            "contact_info": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter contact information",
                }
            ),
            "documentation_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com/documentation",
                }
            ),
            "pictures": forms.FileInput(attrs={"class": "form-control"}),
        }


class CommoditySelectForm(forms.Form):
    """Form for selecting multiple commodities."""

    commodities = forms.ModelMultipleChoiceField(
        queryset=Commodity.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        required=False,
    )


class TagForm(forms.ModelForm):
    """Form for creating new tags."""

    class Meta:
        model = Tag
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter tag name"}
            )
        }
