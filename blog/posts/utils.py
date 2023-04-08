from blog.models import PurposePost, RelationshipPost, Fiction, Newsletter


def search_posts(query):
    purpose_posts = PurposePost.query.filter(
        (PurposePost.title.like(f"%{query}%")) |
        (PurposePost.body.like(f"%{query}%"))
    ).all()

    relationship_posts = RelationshipPost.query.filter(
        (RelationshipPost.title.like(f"%{query}%")) |
        (RelationshipPost.body.like(f"%{query}%"))
    ).all()

    fictions = Fiction.query.filter(
        (Fiction.title.like(f"%{query}%")) |
        (Fiction.body.like(f"%{query}%"))
    ).all()

    newsletters = Newsletter.query.filter(
        (Fiction.title.like(f"%{query}%")) |
        (Fiction.body.like(f"%{query}%"))
    ).all()

    blog_posts = purpose_posts + relationship_posts + fictions + newsletters
    return blog_posts