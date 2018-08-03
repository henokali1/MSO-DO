import dbconnector as db

element_len = {
	'id': 72,
	'req_by': 57,
	'section': 24,
	'department_head': 27,
	'location': 23,
	'description_of_service_as': 180
}

# Checks if the given MSO is approved by both TSM and TSS.
def can_edit(id):
    return (db.get_mso(id)['tsm_approval']) == 1 and (db.get_mso(id)['supervisor_approval'] == 1)

# Check if current user is authorized to delete the given MSO
def can_delete(id, session):
	user_info = db.get_user_by_email(session['email'])
	current_user = user_info['first_name'] + ' ' + user_info['last_name']
	approval = (db.get_mso(id)['tsm_approval']) == None and (db.get_mso(id)['supervisor_approval'] == None)
	return((current_user == db.get_mso(id)['posted_by']) and approval)

def a4_len_calc(element, value):
	try:
		return value +  (element_len[element] - len(value))*' '
	except:
		return str(value) +  (element_len[element] - len(str(value)))*' '

def a4_formatter(id):
	mso_formatted = {}
	mso = db.get_mso(id)

	mso_formatted['id'] = 'CNS-' + a4_len_calc('id', mso['id'])
	mso_formatted['mso_req_date'] = str(mso['posted_on']).replace(' ',',').split(',')[0]
	mso_formatted['mso_req_time'] = str(mso['posted_on']).replace(' ',',').split(',')[1]
	mso_formatted['requested_by'] = a4_len_calc('req_by', mso['requested_by'])
	mso_formatted['section'] = a4_len_calc('section', mso['section'])
	mso_formatted['department_head'] = a4_len_calc('department_head', mso['department_head'])
	mso_formatted['location'] = a4_len_calc('location', mso['location'])
	#mso_formatted['description_of_service'] = a4_len_calc('description_of_service', mso['description_of_service'])


	return mso_formatted
