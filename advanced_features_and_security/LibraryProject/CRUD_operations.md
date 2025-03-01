from bookshelf.models import Book

# create
q = Book(title="1949", author="George Orwell", published_year=1949)
q.save()

# read
Book.objects.all()

# update
q = Book.objects.get(title="1949")
q.title = "Nineteen Eighty-Four"
q.save()

# delete
q = Book.objects.get(title="Nineteen Eight-four")
q.delete()



