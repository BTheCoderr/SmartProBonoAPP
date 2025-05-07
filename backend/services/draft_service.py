from datetime import datetime, timedelta
from models.draft import Draft
from database import db

class DraftService:
    def save_draft(self, user_id, form_type, data, timestamp=None):
        """Save a form draft."""
        if timestamp is None:
            timestamp = datetime.utcnow().timestamp()

        # Check for existing draft
        existing_draft = Draft.query.filter_by(
            user_id=user_id,
            form_type=form_type
        ).first()

        if existing_draft:
            existing_draft.data = data
            existing_draft.timestamp = timestamp
            existing_draft.updated_at = datetime.utcnow()
            draft = existing_draft
        else:
            draft = Draft(
                user_id=user_id,
                form_type=form_type,
                data=data,
                timestamp=timestamp
            )
            db.session.add(draft)

        try:
            db.session.commit()
            return draft
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to save draft: {str(e)}")

    def get_latest_draft(self, user_id, form_type):
        """Get the latest draft for a form type."""
        return Draft.query.filter_by(
            user_id=user_id,
            form_type=form_type
        ).order_by(Draft.timestamp.desc()).first()

    def get_all_drafts(self, user_id, form_type):
        """Get all drafts for a form type."""
        return Draft.query.filter_by(
            user_id=user_id,
            form_type=form_type
        ).order_by(Draft.timestamp.desc()).all()

    def delete_draft(self, user_id, form_type, draft_id):
        """Delete a specific draft."""
        draft = Draft.query.filter_by(
            id=draft_id,
            user_id=user_id,
            form_type=form_type
        ).first()

        if draft:
            try:
                db.session.delete(draft)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Failed to delete draft: {str(e)}")

    def delete_drafts(self, user_id, form_type):
        """Delete all drafts for a form type."""
        try:
            Draft.query.filter_by(
                user_id=user_id,
                form_type=form_type
            ).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to delete drafts: {str(e)}")

    def cleanup_old_drafts(self, days=30):
        """Clean up drafts older than specified days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        try:
            Draft.query.filter(Draft.updated_at < cutoff_date).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to cleanup old drafts: {str(e)}") 