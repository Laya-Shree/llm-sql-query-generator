few_shots = [
    {
        'Question': "How many t-shirts do we have left for nike in extra small size and white color?",
        'SQLQuery': "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND size = 'XS' AND color = 'White';",
        'SQLResult': "Result of the SQL Query",
        'Answer':"11"
    },
    {
        'Question': "If we have to sell all the Levi's T-shirts today with discounts applied. How much revenue our store will generate (post discounts)?",
        'SQLQuery': "SELECT sum(a.total_amount*((100-COALESCE(discounts.pct_discount,0))/100)) AS total_revenue FROM ( SELECT sum(price*stock_quantity) AS total_amount, t_shirt_id FROM t_shirts WHERE brand = 'Levi' GROUP BY t_shirt_id ) a LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id",
        'SQLResult': "Result of the SQL Query",
        'Answer':"20107.10"
    },
    {
        'Question': "What is the highest discount in terms of money that is given?",
        'SQLQuery': "SELECT MAX(price*pct_discount/100) AS discount_amount FROM t_shirts t JOIN discounts d ON t.t_shirt_id = d.t_shirt_id;",
        'SQLResult': "Result of the SQL Query",
        'Answer':"12.60"
    },

]