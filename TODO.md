# plan for development of frontend

### feature wishes
- [] CRUD operations 
    - [] create
    - [] read
    - [] update
    - [] delete
- (probably not much else w the limited time)

### design ideas
page split into 2 columns:
    left: 4 buttons: add product (active), see details (of product) (greyed out), update product (grey), delete product (grey)
    right: table of all items in db
        - consider load animation for if theres a lot of data to b gathered

UX flow when selecting item:
    - presented list of products info in db (ID, type, name, last updated, created), click item in table to select it
    - buttons became active once an item is selected: 
        - see details (the product's fields -> will depend on product type, so cant be in main table), 
        - update this product
        - delete this product
    
UX flow when see details:
    - either go to new page w fields similar to add and update that are filled out, or somehow present info on main page
    - there IS a lot of space under the 4 buttons

UX flow when adding item:
    - omnipresent button to 'add new product' is pressed
    - goes to new page, maybe (url)/add, with text forms and a submit button

UX flow when update button is pressed:
    - goes to page similar to add product (maybe (url)/update/(product id)), with the fields already filled out for the selected item
    - user can change stuff and click submit button

UX flow when delete button:
    - ARE U SURE? prompt
    - if yes -> refresh table of db items (after deleting in backend ofc)