#### Written in Python 3.11


Консольная система управления библиотекой позваляющая добавлять/удалять записи о книгах в базе данных библиотеки, а так же изменять статус наличия книги в библиотеке.

##### Функции:

|Команда|Функция|
|----|----|
| add | добавить книгу |
| delete **X** | удалить книгу с id **X** |
| find **X** | найти книгу по автору, названию или году публикации переданному в **X** |
| find_title **X** | найти книгу по названию **X** |
| find_author **X** | найти книгу по автору **X** |
| find_year **X** | найти книгу по году публикации **X** |
| show_all | показать все книге о которых есть записи в базе |
| change_status **X** | изменить статус наличия книги в библиотеки с id **X** на противоположный |
| help | показать список доступных комманд |

---
A console system of library managment that allows to add/delete records about books in the library's data base, as well as to change availability status of specific books.

##### Features:

|Command|Function|
|----|----|
| add | add a book |
| delete **X** | delete a book with id **X** |
| find **X** | find a book by its title, author or the year when the book was published, passed in **X** |
| find_title **X** | find a book by its title passed in **X** |
| find_author **X** | find a book by its author passed in **X** |
| find_year **X** | find a book passed in the year when it was published passed in **X** |
| show_all | show the list of all books recorded in the data base |
| change_status **X** | change the availability status of a book with id passed in **X** |
| help | show the list of available commands |