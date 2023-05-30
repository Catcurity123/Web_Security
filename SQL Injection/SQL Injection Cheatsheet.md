
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

If the application doesn't implement any defenses against SQL injection, the attacker can construct an attack like:

```
https://insecure-website.com/products?category=Gifts'--
```

Which will result in the SQL query

```SQL
SELECT * FROM products WHERE category = 'Gifts' --' And released = 1
```