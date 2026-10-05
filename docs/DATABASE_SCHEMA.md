\# Fraud Transaction Review System - Database Schema



\## Database Overview



The Fraud Transaction Review System uses SQLite for persistent application data. The database contains three primary application tables: `users`, `transactions`, and `reviews`.



\## Entity Relationship Diagram



```text

+-------------------+

|       users       |

+-------------------+

| PK user\_id        |

|    username       |

|    password\_hash  |

|    full\_name      |

|    role           |

+---------+---------+

&#x20;         |

&#x20;         | 1

&#x20;         |

&#x20;         | many

+---------v---------+

|      reviews      |

+-------------------+

| PK review\_id      |

| FK transaction\_id |

| FK reviewer\_id    |

|    decision       |

|    review\_notes   |

|    reviewed\_at    |

+---------+---------+

&#x20;         ^

&#x20;         | many

&#x20;         |

&#x20;         | 1

+---------+---------+

|   transactions    |

+-------------------+

| PK transaction\_id |

|    account\_id     |

|    transaction\_date|

|    merchant       |

|    amount         |

|    location       |

|    transaction\_type|

|    fraud\_score    |

|    status         |

+-------------------+

