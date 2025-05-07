import pytest
from datetime import datetime, timedelta
from services.draft_service import DraftService
from models.draft import Draft

@pytest.fixture
def draft_service():
    return DraftService()

@pytest.fixture
def sample_draft_data():
    return {
        'user_id': 1,
        'form_type': 'small_claims',
        'data': {
            'plaintiff_name': 'John Doe',
            'claim_amount': 5000
        },
        'timestamp': datetime.utcnow().timestamp()
    }

def test_save_draft(draft_service, sample_draft_data, db_session):
    # Test saving new draft
    draft = draft_service.save_draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type'],
        data=sample_draft_data['data'],
        timestamp=sample_draft_data['timestamp']
    )

    assert draft.id is not None
    assert draft.user_id == sample_draft_data['user_id']
    assert draft.form_type == sample_draft_data['form_type']
    assert draft.data == sample_draft_data['data']
    assert draft.timestamp == sample_draft_data['timestamp']

    # Test updating existing draft
    updated_data = {**sample_draft_data['data'], 'claim_amount': 6000}
    updated_draft = draft_service.save_draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type'],
        data=updated_data
    )

    assert updated_draft.id == draft.id
    assert updated_draft.data['claim_amount'] == 6000

def test_get_latest_draft(draft_service, sample_draft_data, db_session):
    # Save multiple drafts
    draft1 = draft_service.save_draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type'],
        data=sample_draft_data['data'],
        timestamp=datetime.utcnow().timestamp()
    )

    updated_data = {**sample_draft_data['data'], 'claim_amount': 6000}
    draft2 = draft_service.save_draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type'],
        data=updated_data,
        timestamp=datetime.utcnow().timestamp() + 1000
    )

    latest_draft = draft_service.get_latest_draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type']
    )

    assert latest_draft.id == draft2.id
    assert latest_draft.data['claim_amount'] == 6000

def test_get_all_drafts(draft_service, sample_draft_data, db_session):
    # Save multiple drafts
    draft1 = draft_service.save_draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type'],
        data=sample_draft_data['data']
    )

    draft2 = draft_service.save_draft(
        user_id=sample_draft_data['user_id'],
        form_type='fee_waiver',
        data={'applicant_name': 'Jane Doe'}
    )

    # Get all drafts for small_claims
    drafts = draft_service.get_all_drafts(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type']
    )

    assert len(drafts) == 1
    assert drafts[0].id == draft1.id

def test_delete_draft(draft_service, sample_draft_data, db_session):
    # Save a draft
    draft = draft_service.save_draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type'],
        data=sample_draft_data['data']
    )

    # Delete the draft
    draft_service.delete_draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type'],
        draft_id=draft.id
    )

    # Verify draft is deleted
    assert draft_service.get_latest_draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type']
    ) is None

def test_delete_drafts(draft_service, sample_draft_data, db_session):
    # Save multiple drafts
    draft_service.save_draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type'],
        data=sample_draft_data['data']
    )

    draft_service.save_draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type'],
        data={'plaintiff_name': 'Jane Doe'}
    )

    # Delete all drafts
    draft_service.delete_drafts(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type']
    )

    # Verify all drafts are deleted
    drafts = draft_service.get_all_drafts(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type']
    )
    assert len(drafts) == 0

def test_cleanup_old_drafts(draft_service, sample_draft_data, db_session):
    # Save an old draft
    old_draft = Draft(
        user_id=sample_draft_data['user_id'],
        form_type=sample_draft_data['form_type'],
        data=sample_draft_data['data']
    )
    old_draft.updated_at = datetime.utcnow() - timedelta(days=31)
    db_session.add(old_draft)
    db_session.commit()

    # Save a recent draft
    recent_draft = draft_service.save_draft(
        user_id=sample_draft_data['user_id'],
        form_type='fee_waiver',
        data={'applicant_name': 'Jane Doe'}
    )

    # Clean up old drafts
    draft_service.cleanup_old_drafts(days=30)

    # Verify old draft is deleted but recent draft remains
    assert Draft.query.get(old_draft.id) is None
    assert Draft.query.get(recent_draft.id) is not None 