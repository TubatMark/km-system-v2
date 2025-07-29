// View Resource Modal Controller
class ViewResourceModal {
    constructor() {
        this.modal = null;
        this.currentResource = null;
        this.init();
    }

    init() {
        this.modal = new bootstrap.Modal(document.getElementById('viewResourceModal'));
    }

    // Main method to show resource details
    showResource(resourceSlug) {
        this.showLoading();
        this.modal.show();
        
        // Fetch resource data (replace with your actual API endpoint)
        this.fetchResourceData(resourceSlug)
            .then(data => {
                if (!data) {
                    throw new Error('No data received from server');
                }
                this.populateModal(data);
                this.hideLoading();
            })
            .catch(error => {
                console.error('Error fetching resource:', error);
                this.showError(error.message || 'Unknown error occurred');
            });
    }

    showLoading() {
        document.getElementById('loadingState').classList.remove('d-none');
        document.getElementById('resourceContent').classList.add('d-none');
    }

    hideLoading() {
        document.getElementById('loadingState').classList.add('d-none');
        document.getElementById('resourceContent').classList.remove('d-none');
    }

    showError(message = 'Unable to load resource details. Please try again.') {
        document.getElementById('loadingState').innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-exclamation-triangle text-warning fa-3x mb-3"></i>
                <h5>Error Loading Resource</h5>
                <p class="text-muted">${message}</p>
                <button class="btn btn-primary" onclick="location.reload()">Retry</button>
            </div>
        `;
    }

    // Fetch resource data from your Django backend
    async fetchResourceData(slug) {
        const response = await fetch(`/admin/view-resource-modal/${slug}/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch resource data');
        }
        
        const data = await response.json();
        return data;
    }

    // Populate modal with resource data
    populateModal(resource) {
        this.currentResource = resource;
        
        // Set title and basic info - these come from the Django view processing
        document.getElementById('resourceTitle').textContent = resource.title || 'Untitled Resource';
        document.getElementById('resourceDescription').textContent = resource.description || 'No description available';
        document.getElementById('resourceTypeText').textContent = resource.resource_type_display || 'Unknown Type';
        document.getElementById('resourceTypeBadge').textContent = resource.resource_type_display || 'Unknown';
        
        // Set icon based on resource type
        this.setResourceIcon(resource.resource_type);
        
        // Set status badges
        this.setStatusBadges(resource);
        
        // Set dates
        this.setDates(resource);
        
        // Set keywords
        this.setKeywords(resource.keywords);
        
        // Set tags and commodities
        this.setTagsAndCommodities(resource.tags, resource.commodities);
        
        // Set quick info
        this.setQuickInfo(resource);
        
        // Set resource-specific content
        this.setResourceSpecificContent(resource);
    }

    setResourceIcon(resourceType) {
        const iconMap = {
            'event': 'fas fa-calendar-alt',
            'webinar': 'fas fa-video',
            'news': 'fas fa-newspaper',
            'policy': 'fas fa-gavel',
            'publication': 'fas fa-file-alt',
            'technology': 'fas fa-cog',
            'project': 'fas fa-project-diagram',
            'training': 'fas fa-chalkboard-teacher',
            'media': 'fas fa-photo-video',
            'map': 'fas fa-map',
            'info_system': 'fas fa-desktop',
            'product': 'fas fa-box'
        };
        
        const iconClass = iconMap[resourceType] || 'fas fa-file-alt';
        const iconElement = document.getElementById('resourceTypeIcon');
        if (iconElement) {
            iconElement.innerHTML = `<i class="${iconClass}"></i>`;
        }
    }

    setStatusBadges(resource) {
        const approvalBadge = document.getElementById('approvalBadge');
        const featuredBadge = document.getElementById('featuredBadge');
        
        if (approvalBadge) {
            if (resource.is_approved) {
                approvalBadge.className = 'badge bg-success me-2';
                approvalBadge.innerHTML = '<i class="fas fa-check me-1"></i>Approved';
            } else {
                approvalBadge.className = 'badge bg-warning me-2';
                approvalBadge.innerHTML = '<i class="fas fa-clock me-1"></i>Pending';
            }
        }
        
        if (featuredBadge) {
            if (resource.is_featured) {
                featuredBadge.className = 'badge bg-danger me-2';
                featuredBadge.innerHTML = '<i class="fas fa-star me-1"></i>Featured';
                featuredBadge.classList.remove('d-none');
            } else {
                featuredBadge.classList.add('d-none');
            }
        }
    }

    setDates(resource) {
        const createdDate = resource.created_at ? new Date(resource.created_at).toLocaleDateString() : 'Unknown';
        const updatedDate = resource.updated_at ? 
            `Updated: ${new Date(resource.updated_at).toLocaleDateString()}` : '';
        
        this.setElementText('createdDate', createdDate);
        this.setElementText('updatedDate', updatedDate);
    }

    setKeywords(keywords) {
        const keywordsSection = document.getElementById('keywordsSection');
        const keywordsTags = document.getElementById('keywordsTags');
        
        if (keywords && keywords.trim()) {
            const keywordList = keywords.split(',').map(k => k.trim()).filter(k => k);
            if (keywordsTags) {
                keywordsTags.innerHTML = keywordList.map(keyword => 
                    `<span class="keywords-tag">${keyword}</span>`
                ).join('');
            }
            if (keywordsSection) {
                keywordsSection.classList.remove('d-none');
            }
        } else {
            if (keywordsSection) {
                keywordsSection.classList.add('d-none');
            }
        }
    }

    setTagsAndCommodities(tags, commodities) {
        // Set all tags
        const allTagsContainer = document.getElementById('allTags');
        if (allTagsContainer) {
            if (tags && tags.length > 0) {
                allTagsContainer.innerHTML = tags.map(tag => 
                    `<span class="keywords-tag">${tag.name}</span>`
                ).join('');
            } else {
                allTagsContainer.innerHTML = '<span class="text-muted">No tags assigned</span>';
            }
        }
        
        // Set related commodities
        const commoditiesContainer = document.getElementById('relatedCommodities');
        if (commoditiesContainer) {
            if (commodities && commodities.length > 0) {
                commoditiesContainer.innerHTML = commodities.map(commodity => 
                    `<span class="commodity-tag">${commodity.commodity_name}</span>`
                ).join('');
            } else {
                commoditiesContainer.innerHTML = '<span class="text-muted">No commodities assigned</span>';
            }
        }
    }

    setQuickInfo(resource) {
        const quickInfoContent = document.getElementById('quickInfoContent');
        if (!quickInfoContent) return;
        
        let quickInfo = `
            <div class="detail-item">
                <div class="detail-label">Resource Type</div>
                <div class="detail-value">${resource.resource_type_display || 'Unknown'}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Status</div>
                <div class="detail-value">
                    <span class="status-indicator ${resource.is_approved ? 'status-approved' : 'status-pending'}"></span>
                    ${resource.is_approved ? 'Approved' : 'Pending Review'}
                </div>
            </div>
        `;
        
        if (resource.created_by) {
            quickInfo += `
                <div class="detail-item">
                    <div class="detail-label">Created By</div>
                    <div class="detail-value">${resource.created_by}</div>
                </div>
            `;
        }
        
        quickInfoContent.innerHTML = quickInfo;
    }

    setResourceSpecificContent(resource) {
        // Hide all resource type detail sections first
        const allDetailSections = document.querySelectorAll('.resource-type-details');
        allDetailSections.forEach(section => section.classList.add('d-none'));
        
        // Map resource types to section IDs (handle special cases)
        const sectionIdMap = {
            'event': 'eventDetails',
            'webinar': 'webinarDetails',
            'news': 'newsDetails',
            'publication': 'publicationDetails',
            'technology': 'technologyDetails',
            'project': 'projectDetails',
            'policy': 'policyDetails',
            'training': 'trainingDetails',
            'media': 'mediaDetails',
            'product': 'productDetails',
            'info_system': 'infoSystemDetails',
            'map': 'mapDetails'
        };
        
        // Show the appropriate section based on resource type
        const sectionId = sectionIdMap[resource.resource_type];
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.remove('d-none');
            this.populateResourceTypeData(resource);
        }
    }

    populateResourceTypeData(resource) {
        switch (resource.resource_type) {
            case 'event':
                this.populateEventData(resource.event_data);
                break;
            case 'webinar':
                this.populateWebinarData(resource.webinar_data);
                break;
            case 'news':
                this.populateNewsData(resource.news_data);
                break;
            case 'publication':
                this.populatePublicationData(resource.publication_data);
                break;
            case 'technology':
                this.populateTechnologyData(resource.technology_data);
                break;
            case 'project':
                this.populateProjectData(resource.project_data);
                break;
            case 'policy':
                this.populatePolicyData(resource.policy_data);
                break;
            case 'training':
                this.populateTrainingData(resource.training_data);
                break;
            case 'media':
                this.populateMediaData(resource.media_data);
                break;
            case 'product':
                this.populateProductData(resource.product_data);
                break;
            case 'info_system':
                this.populateInfoSystemData(resource.info_system_data);
                break;
            case 'map':
                this.populateMapData(resource.map_data);
                break;
        }
    }

    // Helper method to toggle section visibility
    toggleSectionVisibility(sectionId, condition, populateCallback) {
        const section = document.getElementById(sectionId);
        if (!section) return;
        
        if (condition) {
            section.classList.remove('d-none');
            if (populateCallback) populateCallback();
        } else {
            section.classList.add('d-none');
        }
    }

    // Individual data population methods for each resource type
    populateEventData(data) {
        if (!data) {
            return;
        }
        
        this.setElementText('eventVenue', data.venue);
        this.setElementText('eventOrganizer', data.organizer);
        this.setElementText('eventType', data.event_type);
        this.setElementText('eventStartDate', data.start_date ? new Date(data.start_date).toLocaleString() : 'Not specified');
        this.setElementText('eventEndDate', data.end_date ? new Date(data.end_date).toLocaleString() : 'Not specified');
        
        this.toggleSectionVisibility('eventDocumentationSection', data.documentation_link, () => {
            this.setElementHTML('eventDocumentation', 
                `<a href="${data.documentation_link}" target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-external-link-alt me-1"></i>View Documentation
                </a>`
            );
        });
        
        this.toggleSectionVisibility('eventPicturesSection', data.pictures, () => {
            const img = document.getElementById('eventPictures');
            if (img) img.src = data.pictures;
        });
    }

    populateWebinarData(data) {
        if (!data) return;
        
        this.setElementText('webinarSpeaker', data.speaker);
        this.setElementText('webinarPlatform', data.platform);
        this.setElementText('webinarDuration', data.duration ? `${data.duration} minutes` : 'Not specified');
        this.setElementText('webinarDate', data.date ? new Date(data.date).toLocaleString() : 'Not specified');
        
        this.toggleSectionVisibility('webinarAttendanceSection', data.attendance, () => {
            this.setElementText('webinarAttendance', `${data.attendance} participants`);
        });
        
        this.toggleSectionVisibility('webinarDocumentationSection', data.documentation_link, () => {
            this.setElementHTML('webinarDocumentation', 
                `<a href="${data.documentation_link}" target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-play me-1"></i>View Recording
                </a>`
            );
        });
        
        this.toggleSectionVisibility('webinarPicturesSection', data.pictures, () => {
            const img = document.getElementById('webinarPictures');
            if (img) img.src = data.pictures;
        });
    }

    populateNewsData(data) {
        if (!data) return;
        
        this.setElementText('newsHeadline', data.headline);
        this.setElementText('newsAuthor', data.author);
        this.setElementText('newsContent', data.content);
        
        this.toggleSectionVisibility('newsPositionSection', data.position, () => {
            this.setElementText('newsPosition', data.position);
        });
        
        this.toggleSectionVisibility('newsSourceSection', data.source, () => {
            this.setElementHTML('newsSource', 
                `<a href="${data.source}" target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-external-link-alt me-1"></i>View Original Source
                </a>`
            );
        });
        
        this.toggleSectionVisibility('newsFeaturedImageSection', data.featured_image, () => {
            const img = document.getElementById('newsFeaturedImage');
            if (img) img.src = data.featured_image;
        });
    }

    populatePublicationData(data) {
        if (!data) return;
        
        this.setElementText('publicationAuthor', data.author);
        this.setElementText('publicationDate', data.date_published ? new Date(data.date_published).toLocaleDateString() : 'Not specified');
        this.setElementText('publicationType', data.publication_type_display);
        
        this.toggleSectionVisibility('publicationPublisherSection', data.publisher, () => {
            this.setElementText('publicationPublisher', data.publisher);
        });
        
        this.toggleSectionVisibility('publicationDoiSection', data.doi, () => {
            this.setElementHTML('publicationDoi', 
                `<a href="https://doi.org/${data.doi}" target="_blank" class="text-decoration-none">${data.doi}</a>`
            );
        });
        
        this.toggleSectionVisibility('publicationIsbnSection', data.isbn, () => {
            this.setElementText('publicationIsbn', data.isbn);
        });
        
        this.toggleSectionVisibility('publicationFileSection', data.file, () => {
            this.setElementHTML('publicationFile', 
                `<a href="${data.file}" target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-file-pdf me-1"></i>Download PDF
                </a>`
            );
        });
        
        this.toggleSectionVisibility('publicationDescriptionSection', data.description, () => {
            this.setElementText('publicationDescription', data.description);
        });
    }

    populateTechnologyData(data) {
        if (!data) return;
        
        this.setElementText('technologyName', data.technologies);
        this.setElementText('technologyProducts', data.products);
        this.setElementHTML('technologyAdoptionStatus', 
            `<span class="badge ${data.adoption_status === 'adopted' ? 'bg-success' : 'bg-warning'}">
                ${data.adoption_status_display || 'Unknown'}
            </span>`
        );
        this.setElementText('technologyYearIntroduced', data.year_introduced);
        
        this.toggleSectionVisibility('technologyIpAssetSection', data.ip_asset, () => {
            this.setElementText('technologyIpAsset', data.ip_asset);
        });
        
        this.toggleSectionVisibility('technologyFundingSection', data.funding_source_display, () => {
            this.setElementText('technologyFundingSource', data.funding_source_display);
        });
        
        this.toggleSectionVisibility('technologyExpertSection', data.experts_email, () => {
            this.setElementHTML('technologyExpertEmail', 
                `<a href="mailto:${data.experts_email}" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-envelope me-1"></i>${data.experts_email}
                </a>`
            );
        });
        
        this.toggleSectionVisibility('technologyDescriptionSection', data.brief_description, () => {
            this.setElementText('technologyDescription', data.brief_description);
        });
        
        this.toggleSectionVisibility('technologySupportSection', data.support_facilities, () => {
            this.setElementText('technologySupportFacilities', data.support_facilities);
        });
        
        this.toggleSectionVisibility('technologyExpertsSection', data.available_experts, () => {
            this.setElementText('technologyAvailableExperts', data.available_experts);
        });
        
        this.toggleSectionVisibility('technologyPicturesSection', data.pictures, () => {
            const img = document.getElementById('technologyPictures');
            if (img) img.src = data.pictures;
        });
    }

    populateProjectData(data) {
        if (!data) return;
        
        this.toggleSectionVisibility('projectProgramSection', data.program_title, () => {
            this.setElementText('projectProgramTitle', data.program_title);
        });
        
        this.setElementText('projectTitle', data.project_title);
        this.setElementText('projectLeader', data.project_leader);
        this.setElementHTML('projectStatus', 
            `<span class="badge ${this.getProjectStatusBadge(data.status)}">
                ${data.status_display || data.status || 'Unknown'}
            </span>`
        );
        this.setElementText('projectStartDate', data.start_date ? new Date(data.start_date).toLocaleDateString() : 'Not specified');
        
        this.toggleSectionVisibility('projectEndDateSection', data.end_date, () => {
            this.setElementText('projectEndDate', new Date(data.end_date).toLocaleDateString());
        });
        
        this.toggleSectionVisibility('projectBudgetSection', data.total_approved_budget, () => {
            this.setElementText('projectBudget', `₱${parseFloat(data.total_approved_budget).toLocaleString()}`);
        });
        
        this.toggleSectionVisibility('projectExtensionSection', data.extension_months, () => {
            this.setElementText('projectExtension', `${data.extension_months} months`);
        });
        
        this.toggleSectionVisibility('projectFundingSection', data.source_of_fund, () => {
            this.setElementText('projectFundingSource', data.source_of_fund);
        });
        
        this.toggleSectionVisibility('projectImplementingSection', data.implementing_agency, () => {
            this.setElementText('projectImplementingAgency', data.implementing_agency);
        });
        
        this.toggleSectionVisibility('projectCooperatingSection', data.cooperating_agency, () => {
            this.setElementText('projectCooperatingAgency', data.cooperating_agency);
        });
        
        this.toggleSectionVisibility('projectCollaboratingSection', data.collaborating_agency, () => {
            this.setElementText('projectCollaboratingAgency', data.collaborating_agency);
        });
    }

    populatePolicyData(data) {
        if (!data) return;
        
        this.setElementHTML('policyType', 
            `<span class="badge ${data.policy_type === 'research' ? 'bg-info' : 'bg-success'}">
                ${data.policy_type_display || data.policy_type || 'Unknown'}
            </span>`
        );
        this.setElementText('policyAgency', data.agency);
        this.setElementText('policyYear', data.year);
        this.setElementText('policyDescription', data.description);
        
        this.toggleSectionVisibility('policyAuthorSection', data.author, () => {
            this.setElementText('policyAuthor', data.author);
        });
        
        this.toggleSectionVisibility('policyAdvocacySection', data.advocacy_project, () => {
            this.setElementText('policyAdvocacyProject', data.advocacy_project);
        });
        
        this.toggleSectionVisibility('policyFindingsSection', data.findings, () => {
            this.setElementText('policyFindings', data.findings);
        });
        
        this.toggleSectionVisibility('policyTextSection', data.policy_text, () => {
            this.setElementText('policyText', data.policy_text);
        });
    }

    populateTrainingData(data) {
        if (!data) return;
        
        this.setElementText('trainingTitle', data.title);
        this.setElementText('trainingVenue', data.venue);
        this.setElementText('trainingOrganizer', data.organizer);
        this.setElementText('trainingStartDate', data.start_date ? new Date(data.start_date).toLocaleString() : 'Not specified');
        
        this.toggleSectionVisibility('trainingEndDateSection', data.end_date, () => {
            this.setElementText('trainingEndDate', new Date(data.end_date).toLocaleString());
        });
        
        this.toggleSectionVisibility('trainingSpeakersSection', data.speakers, () => {
            this.setElementText('trainingSpeakers', data.speakers);
        });
        
        this.toggleSectionVisibility('trainingParticipantsSection', data.total_participants, () => {
            this.setElementText('trainingParticipants', data.total_participants);
        });
        
        this.toggleSectionVisibility('trainingDocumentationSection', data.documentation_link, () => {
            this.setElementHTML('trainingDocumentation', 
                `<a href="${data.documentation_link}" target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-external-link-alt me-1"></i>View Materials
                </a>`
            );
        });
        
        this.toggleSectionVisibility('trainingDescriptionSection', data.description, () => {
            this.setElementText('trainingDescription', data.description);
        });
        
        this.toggleSectionVisibility('trainingPicturesSection', data.pictures, () => {
            const img = document.getElementById('trainingPictures');
            if (img) img.src = data.pictures;
        });
    }

    populateMediaData(data) {
        if (!data) return;
        
        this.setElementText('mediaTitle', data.title);
        
        this.toggleSectionVisibility('mediaLinkSection', data.link, () => {
            this.setElementHTML('mediaLink', 
                `<a href="${data.link}" target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-external-link-alt me-1"></i>View Media
                </a>`
            );
        });
    }

    populateProductData(data) {
        if (!data) return;
        
        this.setElementText('productName', data.products);
        this.setElementText('productCompany', data.company);
        this.setElementText('productDescription', data.description);
        
        this.toggleSectionVisibility('productPriceSection', data.price, () => {
            this.setElementText('productPrice', `₱${parseFloat(data.price).toLocaleString()}`);
        });
        
        this.toggleSectionVisibility('productDocumentationSection', data.documentation_link, () => {
            this.setElementHTML('productDocumentation', 
                `<a href="${data.documentation_link}" target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-external-link-alt me-1"></i>View Details
                </a>`
            );
        });
        
        this.toggleSectionVisibility('productPicturesSection', data.pictures, () => {
            const img = document.getElementById('productPictures');
            if (img) img.src = data.pictures;
        });
        
        this.toggleSectionVisibility('productContactSection', data.contact_info, () => {
            this.setElementText('productContactInfo', data.contact_info);
        });
    }

    populateInfoSystemData(data) {
        if (!data) return;
        
        this.setElementText('infoSystemOwner', data.organization_owner);
        
        this.toggleSectionVisibility('infoSystemAgencySection', data.agency, () => {
            this.setElementText('infoSystemAgency', data.agency);
        });
        
        this.toggleSectionVisibility('infoSystemLinkSection', data.link, () => {
            this.setElementHTML('infoSystemLink', 
                `<a href="${data.link}" target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-external-link-alt me-1"></i>Visit System
                </a>`
            );
        });
        
        this.toggleSectionVisibility('infoSystemExplanationSection', data.brief_explanation, () => {
            this.setElementText('infoSystemExplanation', data.brief_explanation);
        });
    }

    populateMapData(data) {
        if (!data) return;
        
        if (data.latitude && data.longitude) {
            this.setElementText('mapCoordinates', `Lat: ${data.latitude}, Lng: ${data.longitude}`);
            const coordinatesSection = document.getElementById('mapCoordinatesSection');
            if (coordinatesSection) coordinatesSection.classList.remove('d-none');
        } else {
            const coordinatesSection = document.getElementById('mapCoordinatesSection');
            if (coordinatesSection) coordinatesSection.classList.add('d-none');
        }
        
        this.toggleSectionVisibility('mapUrlSection', data.map_url, () => {
            this.setElementHTML('mapUrl', 
                `<a href="${data.map_url}" target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-map me-1"></i>View Interactive Map
                </a>`
            );
        });
        
        this.toggleSectionVisibility('mapFileSection', data.map_file, () => {
            this.setElementHTML('mapFile', 
                `<a href="${data.map_file}" target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-download me-1"></i>Download Map
                </a>`
            );
        });
    }

    // Helper methods for setting element content
    setElementText(elementId, text) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = text || 'Not specified';
        }
    }

    setElementHTML(elementId, html) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = html || 'Not available';
        }
    }

    // Helper methods
    getProjectStatusBadge(status) {
        const statusMap = {
            'ongoing': 'bg-primary',
            'completed': 'bg-success',
            'terminated': 'bg-danger'
        };
        return statusMap[status] || 'bg-secondary';
    }

    editResource() {
        if (this.currentResource) {
            // Redirect to edit page or open edit modal
            window.location.href = `/admin/resources/edit/${this.currentResource.slug}/`;
        }
    }

    downloadResource() {
        if (this.currentResource) {
            // Handle download logic based on resource type
            // This could download files, generate PDFs, etc.
            window.open(`/admin/resources/download/${this.currentResource.slug}/`, '_blank');
        }
    }
}

// Initialize the modal controller
document.addEventListener('DOMContentLoaded', function() {
    window.viewResourceModal = new ViewResourceModal();
});

// Function to be called from your table's view buttons
function viewResource(slug) {
    if (window.viewResourceModal) {
        window.viewResourceModal.showResource(slug);
    }
}

// Helper function to get CSRF token (if not already defined elsewhere)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
           }
       }
   }
   return cookieValue;
}