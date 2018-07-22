import dbconnector as db


# Checks if the given MSO is approved by both TSM and TSS.
def can_edit(id):
    return (db.get_mso(id)['tsm_approval']) == 1 and (db.get_mso(id)['supervisor_approval'] == 1)

# Check if current user is authorized to delete the given MSO
def can_delete(id, session):
	user_info = db.get_user_by_email(session['email'])
	current_user = user_info['first_name'] + ' ' + user_info['last_name']
	return(current_user == db.get_mso(id)['posted_by'])
