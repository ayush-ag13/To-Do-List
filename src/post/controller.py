from flask import jsonify, request
from src import db
from sqlalchemy import text
from src.post import post_blueprint
from src.post.model import Post
from src.user.model import User
from flask_jwt_extended import (
	jwt_required,
	get_jwt_identity,
)

@post_blueprint.get('/ping')
@jwt_required()
def ping():
	return jsonify('OK')

@post_blueprint.post('/createPost')
@jwt_required()
def createPost():
	description = request.json.get("description")
	imgLink = request.json.get("imgLink")
	unixTime = request.json.get("unixTime")

	if ((imgLink==None) or (None==unixTime)):
		return jsonify({'success': False, 'message': 'please provide all arguments'})
	
	identity = get_jwt_identity()

	new_post = Post(description=description,imgLink=imgLink,unixTime=unixTime,userId=identity)
	try:
		db.session.add(new_post)
		db.session.commit()
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)})

	return jsonify({'success': True, 'message': 'Post created successfully'})

@post_blueprint.get('/allPosts')
@jwt_required()
def allPosts():
	try:
		lst=[]
		userId = get_jwt_identity()
		user = User.query.filter_by(id=userId).one_or_none()
		if(not user):
			return jsonify({'success': False, 'message': 'user with id=[{}] not present.'.format(userId)})
		
		query = f'''
		select description,imgLink,unixTime,email, p.id as id
		from posts p inner join users u
		on p.userId = u.id
		where u.id = {userId}
		order by unixTime desc
		'''
		with db.engine.connect() as conn:
			lst = conn.execute(text(query))
			lst = lst.mappings().all()
			lst = [dict(row) for row in lst]
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)})
	return jsonify({'success': True,'list':lst})

@post_blueprint.get('/getPost/<int:post_id>')
@jwt_required()
def getPost(post_id):
	try:
		post = Post.query.filter_by(id=post_id).one_or_none()
		if (not post):
			return jsonify({'success': False, 'message': 'post with id=[{}] not present.'.format(post_id)})
		
		userId = get_jwt_identity()
		user = User.query.filter_by(id=userId).one_or_none()
		if(not user):
			return jsonify({'success': False, 'message': 'user with id=[{}] not present.'.format(userId)})
		if(userId!=post.userId):
			return jsonify({'success': False, 'message': 'user with id=[{}] is not the author for post with id=[{}].'.format(userId,post_id)})
		
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)})
	return jsonify({'success': True, 'post': post.as_dict()})

@post_blueprint.delete('/deletePost/<int:post_id>')
@jwt_required()
def deletePost(post_id):
	try:
		post = Post.query.filter_by(id=post_id).one_or_none()
		if (not post):
			return jsonify({'success': False, 'message': 'post with id=[{}] not present.'.format(post_id)})
		
		userId = get_jwt_identity()
		user = User.query.filter_by(id=userId).one_or_none()
		if(not user):
			return jsonify({'success': False, 'message': 'user with id=[{}] not present.'.format(userId)})
		if(userId!=post.userId):
			return jsonify({'success': False, 'message': 'user with id=[{}] is not the author for post with id=[{}].'.format(userId,post_id)})

		db.session.delete(post)
		db.session.commit()
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)})
	return jsonify({'success': True, 'message': 'post with id=[{}] deleted successfully.'.format(post_id)})