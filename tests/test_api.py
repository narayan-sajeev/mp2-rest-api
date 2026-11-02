# Test to ensure CSV meets requirements
def test_upload_csv(client, sample_csv_bytes):
    # Build response to POST /upload
    response = client.post('/upload', files={
        # Payloads are tuple:
        # filename, content, content_type
        'file': (
            'sample_data.csv',
            sample_csv_bytes,
            'text/csv'
        )
    })

    # Ensure status code is 200
    assert response.status_code == 200
    # Convert to JSON using DatasetInfo model
    data = response.json()
    # Ensure row count is 6
    assert data['rows'] == 6
    # Ensure column count is 2
    assert data['columns'] == 2
    # Ensure id is integer
    assert type(data['id']) == int
    # Ensure id is positive
    assert data['id'] > 0

# Test to ensure validation and processing works
def test_process_and_retrieve(client, uploaded_dataset_id, processing_body):
    # Build response to POST /process
    initial_response = client.post(f'/datasets/{uploaded_dataset_id}/process', json=processing_body)

    # Ensure status code is 200
    assert initial_response.status_code == 200
    # Convert to JSON using ProcessingReport model
    data = initial_response.json()
    # Ensure 1 row was removed
    assert data['validation_rows_removed'] == 1
    # Ensure initial row count was 5
    assert data['cleaning_report']['rows_before'] == 5
    # Ensure final row count was 3
    assert data['cleaning_report']['rows_after'] == 3

    # Create GET request
    get_response = client.get(f'/datasets/{uploaded_dataset_id}')

    # Ensure status code is 200
    assert get_response.status_code == 200
    # Convert GET response to JSON using GET dict in main
    get_dict = get_response.json()
    # Ensure that total rows is 3
    assert get_dict['total_rows'] == 3
    # Get data
    get_data = get_dict['data']

    # Define expected records
    # Enter as float so validation succeeds
    expected = [
        {'student_id': 1, 'score': 80.0},
        {'student_id': 2, 'score': 90.0},
        {'student_id': 5, 'score': 85.0}
    ]

    # Ensure the output matches
    assert get_data == expected

# Test to ensure that missing data is handled
def test_retrieve_missing_dataset(client):
    # Build response
    response = client.get('/datasets/9999')
    # Ensure that the status code is 404
    assert response.status_code == 404