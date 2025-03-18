import streamlit as st
import json

def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_library():
    with open("library.json", "w") as file:
        json.dump(library, file, indent=4)
library = load_library()

st.title("Personal Library Manager")
st.write("Easily manage your book collection!")

menu = st.sidebar.radio("Choose an action", [
    "Add a Book", "Remove a Book", "Search a Book", "Display All Books", "View Statistics", "Save & Exit"
])

if menu == "Add a Book":
    st.header("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author Name")
    year = st.number_input("Publication Year", min_value=1000, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Mark as Read")
    
    if st.button("Add Book"):
        library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status})
        save_library()
        st.success("Book added successfully!")
        st.rerun()

elif menu == "Remove a Book":
    st.header("Remove a Book")
    book_titles = [book["title"] for book in library]
    
    if book_titles:
        selected_book = st.selectbox("Select a book to remove", book_titles, key="remove_book")
        
        if st.button("Remove Book"):
            library[:] = [book for book in library if book["title"] != selected_book]
            save_library()
            st.success("Book removed successfully!")
            st.rerun()
    else:
        st.warning("No books available to remove.")

elif menu == "Search a Book":
    st.header("Search for a Book")
    search_term = st.text_input("Enter title or author name")
    
    if st.button("Search"):
        results = [book for book in library if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()]
        
        if results:
            st.write("Matching books found:")
            st.table(results)
        else:
            st.warning("No books found.")

elif menu == "Display All Books":
    st.header("Your Library Collection")
    
    if library:
        st.table(library)
    else:
        st.info("Your library is currently empty. Add books to get started!")

elif menu == "View Statistics":
    st.header("Library Statistics")
    
    total_books = len(library)
    books_read = sum(1 for book in library if book["read"])
    percentage_read = (books_read / total_books * 100) if total_books > 0 else 0
    
    st.write(f"Total Books: {total_books}")
    st.write(f"Books Read: {books_read}")
    st.write(f"Percentage Read: {percentage_read:.2f}%")

elif menu == "Save & Exit":
    save_library()
    st.success("Library saved successfully!")

