from django.db import models
from category.models import Category
import uuid
from accounts.models import Account

class Author(models.Model):
  author_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  author_name = models.CharField(max_length=255)


class Book(models.Model):
  book_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  title = models.CharField(max_length=255)
  slug = models.SlugField(max_length=60, unique=True) 
  image = models.ImageField(upload_to="images/books_img/") 
  description = models.TextField()
  publishers = models.JSONField()
  format = models.CharField(max_length=255)
  page_count = models.IntegerField()
  average_rating = models.FloatField(default=0.0)
  price = models.FloatField()
  publication_date = models.DateTimeField()
  ISBN = models.CharField(max_length=20)
  stocks_available = models.IntegerField()
  language = models.CharField(max_length=50)
  created_on = models.DateTimeField(auto_now_add=True)
  modified_on = models.DateTimeField(auto_now=True)
  authorList = models.ManyToManyField(Author)
  genreList = models.ManyToManyField(Category)
  
  @property
  def author_names(self):
      authors = self.authorList.all()
      if authors:
          return ', '.join(author.author_name for author in authors)
      else:
          return ''

  @property
  def genre_names(self):
      category = self.genreList.all()
      if category:
          return ', '.join(genre.category_name for genre in category)
      else:
          return ''

class Review(models.Model):
  review_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  user =models.ForeignKey(Account, on_delete=models.CASCADE)
  rating = models.IntegerField()
  review_text = models.TextField()
  review_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
  comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  user =models.ForeignKey(Account, on_delete=models.CASCADE)
  comment_text = models.TextField()
  comment_date = models.DateTimeField(auto_now_add=True)



