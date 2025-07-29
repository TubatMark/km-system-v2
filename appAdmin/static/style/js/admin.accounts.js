document.addEventListener('DOMContentLoaded', function () {
    // Initialize the pie charts using jQuery
    $('.user-chart-pie').each(function () {
        const $this = $(this);
        const percent = $this.data('percent');
        const barColor = $this.attr('id') === 'generalUserChart' ? '#f44336' :
            $this.attr('id') === 'cmiUserChart' ? '#2196f3' : '#ff9800';

        $this.easyPieChart({
            size: 80,
            barColor: barColor,
            scaleColor: false,
            trackColor: '#e5e5e5',
            lineWidth: 5,
            lineCap: 'round',
            animate: 1000
        });
    });

    // Function to handle user deletion confirmation
    $('.delete-btn').on('click', function (event) {
        event.preventDefault(); // Prevent the default link behavior

        const deleteUrl = $(this).attr('href');

        Swal.fire({
            title: 'Are you sure?',
            text: 'Do you really want to delete this user? This action cannot be undone.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                // If confirmed, proceed with the deletion
                window.location.href = deleteUrl;
            }
        });
    });

    // Initialize the DataTable
    const accountsTable = $('#accountsTable').DataTable({
        language: {
            lengthMenu: 'Show _MENU_ entries',
            search: '',
            searchPlaceholder: 'Search...'
        },
        lengthMenu: [
            [7, 10, 25, -1],
            [7, 10, 25, 'All']
        ],
        paging: true,
        lengthChange: true,
        autoWidth: false,
        bInfo: true,
        bSort: true,
        responsive: true,
        buttons: [
            {
                text: 'CSV',
                extend: 'csv',
                className: 'btn-sm'
            },
            {
                text: 'PDF',
                extend: 'pdf',
                className: 'btn-sm'
            },
            {
                text: 'ADD',
                className: 'btn btn-primary btn-sm',
                action: function () {
                    $('#accountRegistrationModal').modal('show');
                }
            }
        ],
        dom:
            '<"row"<"col-md-3"l><"col-md-9 text-right"B>>' +
            '<"row"<"col-md-12"tr>>' +
            '<"row"<"col-md-5"i><"col-md-7"p>>'
    });

    // Ensure proper styling for DataTable elements
    $('.dataTables_length').addClass('float-left d-inline-block').css('width', 'auto');
    $('.dt-buttons').addClass('float-right d-inline-block');

    // Custom search functionality
    $('#searchButton').on('click', function () {
        filterTable();
    });

    // Also filter when user types in any of the search fields
    $('#search_user_id, #search_name, #search_institution').on('keyup', function () {
        filterTable();
    });

    // Function to handle table filtering
    function filterTable() {
        const userId = $('#search_user_id').val().toLowerCase();
        const name = $('#search_name').val().toLowerCase();
        const institution = $('#search_institution').val().toLowerCase();

        // Use DataTables API for more efficient searching
        accountsTable.search('').draw(); // Clear any existing search

        // Apply custom filtering
        $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
            const rowUserId = data[0].toLowerCase();
            const rowName = data[1].toLowerCase();
            const rowInstitution = data[4].toLowerCase();

            const userIdMatch = userId === '' || rowUserId.includes(userId);
            const nameMatch = name === '' || rowName.includes(name);
            const institutionMatch = institution === '' || rowInstitution.includes(institution);

            return userIdMatch && nameMatch && institutionMatch;
        });

        accountsTable.draw();

        // Remove the custom filter after drawing
        $.fn.dataTable.ext.search.pop();
    }

    // Handle view modal data population
    $('.view-btn').on('click', function () {
        const userId = $(this).data('userid');
        const firstName = $(this).data('firstname');
        const middleName = $(this).data('middlename');
        const lastName = $(this).data('lastname');
        const dateJoined = $(this).data('datejoined');
        const userEmail = $(this).data('email');
        const institution = $(this).data('institution');
        const position = $(this).data('position');
        const userType = $(this).data('usertype');
        const sex = $(this).data('sex');
        const gender = $(this).data('gender');
        const dateBirth = $(this).data('birthdate');
        const contactNum = $(this).data('contactnum');
        const highestEduc = $(this).data('highesteduc');
        const specialization = $(this).data('specialization');

        const modal = $('#viewAccountModal');
        modal.find('#id').val(userId);
        modal.find('#first_name').val(firstName);
        modal.find('#middle_name').val(middleName);
        modal.find('#last_name').val(lastName);
        modal.find('#email').val(userEmail);
        modal.find('#institution').val(institution);
        modal.find('#position').val(position);
        modal.find('#user_type').val(userType);
        modal.find('#sex').val(sex);
        modal.find('#gender').val(gender);
        modal.find('#date_birth').val(dateBirth);
        modal.find('#contact_num').val(contactNum);
        modal.find('#highest_educ').val(highestEduc);
        modal.find('#specialization').val(specialization);
    });

    // Handle edit modal data population and form action
    $('.edit-btn').on('click', function () {
        const userId = $(this).data('userid');
        const firstName = $(this).data('firstname');
        const middleName = $(this).data('middlename');
        const lastName = $(this).data('lastname');
        const dateJoined = $(this).data('datejoined');
        const userEmail = $(this).data('email');
        const institution = $(this).data('institution');
        const position = $(this).data('position');
        const userType = $(this).data('usertype');
        const sex = $(this).data('sex');
        const gender = $(this).data('gender');
        const dateBirth = $(this).data('birthdate');
        const contactNum = $(this).data('contactnum');
        const highestEduc = $(this).data('highesteduc');
        const specialization = $(this).data('specialization');

        const modal = $('#editAccountModal');
        modal.find('#id').val(userId);
        modal.find('#first_name').val(firstName);
        modal.find('#middle_name').val(middleName);
        modal.find('#last_name').val(lastName);
        modal.find('#email').val(userEmail);
        modal.find('#institution').val(institution);
        modal.find('#position').val(position);

        // For select elements, we need to select the correct option
        modal.find('#user_type').val(userType.toLowerCase());
        modal.find('#sex').val(sex ? sex.toLowerCase() : '');
        modal.find('#gender').val(gender ? gender.toLowerCase() : '');

        modal.find('#date_birth').val(dateBirth);
        modal.find('#contact_num').val(contactNum);

        // Extract just the education level from "X's Degree"
        const educLevel = highestEduc ? highestEduc.split(' ')[0].toLowerCase() : '';
        modal.find('#highest_educ').val(educLevel);

        modal.find('#specialization').val(specialization);

        // Set the form action URL
        $('#editAccountForm').attr('action', formAction);
    });
});