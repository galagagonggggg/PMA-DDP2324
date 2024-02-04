# Warwick's Dining Facilitites website

A website which manage the warwick's dinning facilities covered these functionalities
1. Facilities detail page (config by each facilities) with customer review (future phrase)
2. Facilities list page with dropdown filter
3. Facilities landing page
* Recommend facilities
* Popular facilities
* Filter by type
* Dropdown filter
---
## Prerequisite

- [VS Code with Python Extension](https://code.visualstudio.com/docs/languages/python)
- [Flask (for running the backend API)](https://flask.palletsprojects.com/en/3.0.x/)
- [Python virtual environment (not require but recommend)](https://code.visualstudio.com/docs/python/environments)
---
## Folder with file Structure (second level)

There are two folder which contain all of the html, css, and image which are the frontend stuff that named to align with flask folder structure to make the application able to proceed
1. `static` folder
* Image file : all of the image that use in this website like .png or .jpeg will all store in this folder
* CSS file : 'main.css' is the main file that control all of the styling in this website
2. `templates` folder
* `detail.html` : the facilities detail list screen which display the information in each facilities e.g. contact information, name, menu, location etc. with the future implementation as the customer review functionalities
* `list.html` : the list of warwick's dining facilities display according to the dropdown filter section on the top which is sticky
* `main.html` : the landing page which contain the recommend, popular, filter by type, dropdown filter in the page to promote the warwick's dining facilities
--
## File structure (top level)

These are the main file that is outside the folder mainly in python backend and flask to make the application can proceed
1. `app.py` : this is the main file that contain all of the path and flask API to proceed the application
* `/facilities-landing` : for landing screen to display the data showing on `main.html` and also `POST` method if user tab on find after apply dropdown filter
* `/facilities-list/<number_of_guest>/<open_day>/<open_time>/<is_student_union>/<type_id>` : contain backend logic to filter and return the list with the applyed query parameter to display on 'list.html' and also `POST` method for user that apply the search filter on the 'list.html' page
* `/facilities-detail/<profile_id>` : to display the facilities detail `detail.html` according to each `profile_id` and also customer review part on the future implementation. Furthermore, `POST` method apply when user submit customer review from the screen
2. `dining.db` : the database for the website conssit of these four tables which have to run with sqlite database
* `tbl_dining_profile` : contain all of every dining facilities detail
* `tbl_dining_type` : contain all the type in which display on landing page ex. restaurant, drink
* `tbl_dining_type_mapping` : mapping each dining facilities to each dining type
* (Future Phrase) `tbl_customer_review` : each record of customer review on each facilities
3. `app_minimal.py` and `confirm.py` : use to test that flask able to work
4. `requirement.txt` : file that contain all of the library that should be install to make the library for flask application works
5. `test_app.py` : file for unit test that test the response of every endpoint in both `GET` and `POST` method with various case of parameter mainly generated by ChatGPT with adjust some case to make test case more comprehensive and correct such as filter functionality
