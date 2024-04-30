from django.contrib import admin
from .models import Book, Author, Review, Comment

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_name',)
    search_fields = ('author_name',)

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'author_names',
        'genre_names',
        'format',
        'page_count',
        'average_rating',
        'price',
        'publication_date',
        'ISBN',
        'stocks_available',
        'language',
        'created_on',
        'modified_on',
    )
    list_filter = ('authorList', 'genreList', 'publication_date', 'format', 'language')
    search_fields = ('title', 'authorList__author_name', 'genreList__category_name', 'ISBN')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_on', 'modified_on')
    ordering = ('-modified_on',)
    inlines = [ReviewInline, CommentInline]

    def author_names(self, obj):
        return obj.author_names

    def genre_names(self, obj):
        return obj.genre_names

    author_names.short_description = 'Author(s)'
    genre_names.short_description = 'Genre(s)'
    
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
