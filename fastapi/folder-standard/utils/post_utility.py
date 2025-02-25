def post_data(post_id: int):
    return {
            "id": post_id,
            "title": "foo",
            "content": f"Content for post {post_id}",
            "published": True
            } 

def filter_post(post, searchQuery):
   return[post for post in post if searchQuery in post["title"]]