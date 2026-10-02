from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from blogs.models import Post, Category


class Command(BaseCommand):
    help = "Add sample categories and blog posts to the database"

    def handle(self, *args, **kwargs):

        # ---------------------------------------------------------
        # Create sample user
        # ---------------------------------------------------------

        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@devblogs.com",
                "first_name": "DevBlogs",
                "last_name": "Admin",
            }
        )

        if created:
            user.set_password("admin123")
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    "Created sample user: admin"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Sample user already exists: admin"
                )
            )


        # ---------------------------------------------------------
        # Create categories
        # ---------------------------------------------------------

        categories = {}

        category_data = [
            {
                "name": "Django",
                "description": "Articles about Django web development."
            },
            {
                "name": "Python",
                "description": "Articles about Python programming."
            },
            {
                "name": "DevOps",
                "description": "Articles about Docker, CI/CD, cloud and DevOps."
            },
            {
                "name": "Databases",
                "description": "Articles about SQL, databases and data modelling."
            },
            {
                "name": "Web Development",
                "description": "Articles about web development and HTTP."
            },
        ]

        for data in category_data:

            category, created = Category.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"]
                }
            )

            categories[data["name"]] = category

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created category: {category.name}"
                    )
                )


        # ---------------------------------------------------------
        # Create posts
        # ---------------------------------------------------------

        posts = [

            {
                "title": "Understanding Django Models",
                "category": "Django",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
                "featured": True,
                "content": """
Django models provide a Python-based way of defining the structure
of data stored in a database. A model usually represents a database
table, while each field represents a column.

Models allow developers to work with database records using Python
and Django's ORM instead of writing SQL for every operation.
"""
            },

            {
                "title": "Getting Started with Django ORM",
                "category": "Django",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
                "featured": False,
                "content": """
Django ORM allows developers to interact with a database using
Python objects and methods. Instead of manually writing SQL queries,
we can use methods such as objects.all(), objects.get(), objects.filter(),
create(), update(), and delete().
"""
            },

            {
                "title": "Python Functions Every Developer Should Understand",
                "category": "Python",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
                "featured": False,
                "content": """
Functions allow developers to organize reusable pieces of logic.
A function can accept parameters, perform an operation, and return
a result.

Well-designed functions make applications easier to read, test,
debug, and maintain.
"""
            },

            {
                "title": "Understanding Python Classes",
                "category": "Python",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
                "featured": False,
                "content": """
Classes are a fundamental part of object-oriented programming in
Python. A class defines the structure and behaviour of objects.

Classes allow developers to group related data and functionality
into reusable structures.
"""
            },

            {
                "title": "How HTTP Requests Work",
                "category": "Web Development",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
                "featured": True,
                "content": """
HTTP is the communication protocol used by web browsers, APIs,
and web servers.

When a client makes a request, the server processes the request
and returns a response. Common HTTP methods include GET, POST,
PUT, PATCH, and DELETE.
"""
            },

            {
                "title": "Building Maintainable Web Applications",
                "category": "Web Development",
                "status": Post.Status.DRAFT,
                "published_at": None,
                "featured": False,
                "content": """
Maintainable applications require good project structure,
separation of concerns, meaningful naming, reusable components,
proper error handling, and automated testing.

Django provides several features that help developers organize
large applications effectively.
"""
            },

            {
                "title": "Introduction to Docker for Developers",
                "category": "DevOps",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
                "featured": True,
                "content": """
Docker allows applications and their dependencies to be packaged
into containers. Containers provide a consistent environment for
development, testing, and deployment.

Docker is particularly useful when different developers need to
run the same application environment.
"""
            },

            {
                "title": "Understanding CI/CD Pipelines",
                "category": "DevOps",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
                "featured": False,
                "content": """
CI/CD automates parts of the software development lifecycle.

Continuous Integration allows developers to automatically build
and test code changes. Continuous Delivery or Deployment extends
this process by automatically preparing or deploying applications.
"""
            },

            {
                "title": "SQL Fundamentals for Django Developers",
                "category": "Databases",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
                "featured": False,
                "content": """
SQL is used to communicate with relational databases.

Important SQL operations include SELECT, INSERT, UPDATE, and DELETE.
Understanding SQL helps Django developers understand what is
happening underneath Django's ORM.
"""
            },

            {
                "title": "Database Relationships Explained",
                "category": "Databases",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
                "featured": False,
                "content": """
Relational databases commonly use relationships such as
one-to-one, one-to-many, and many-to-many.

Django represents these relationships using fields such as
OneToOneField, ForeignKey, and ManyToManyField.
"""
            },

            {
                "title": "Why Database Design Matters",
                "category": "Databases",
                "status": Post.Status.DRAFT,
                "published_at": None,
                "featured": False,
                "content": """
Good database design reduces duplication, improves data integrity,
and makes applications easier to maintain.

Before building complex applications, developers should understand
how entities relate to each other and how those relationships should
be represented in the database.
"""
            },

            {
                "title": "Django Migrations Explained",
                "category": "Django",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
                "featured": False,
                "content": """
Django migrations allow developers to track changes made to database
models and apply those changes to the actual database.

The usual workflow is to run makemigrations after changing models
and then run migrate to apply the changes.
"""
            },
        ]


        # ---------------------------------------------------------
        # Insert posts
        # ---------------------------------------------------------

        added = 0
        skipped = 0

        for post in posts:

            if Post.objects.filter(
                title=post["title"]
            ).exists():

                skipped += 1
                continue

            Post.objects.create(
                user=user,
                category=categories[post["category"]],
                title=post["title"],
                content=post["content"],
                status=post["status"],
                published_at=post["published_at"],
                featured=post["featured"],
                views=0,
            )

            added += 1


        # ---------------------------------------------------------
        # Final output
        # ---------------------------------------------------------

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Added {added} posts and skipped {skipped} existing posts."
            )
        )