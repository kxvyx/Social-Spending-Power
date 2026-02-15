# Social Spending Power

A backend API built with FastAPI and SQLAlchemy to track users, groups, and recurring bills to determine disposable income.

# 🚀 Installation & Setup

```bash
git clone [https://github.com/kxvyx/Social-Spending-Power.git](https://github.com/kxvyx/Social-Spending-Power.git)
cd Social-Spending-Power

python -m venv venv
# For Windows
.\venv\Scripts\activate
# For Linux/Mac
source venv/bin/activate

pip install fastapi uvicorn pydantic sqlalchemy

uvicorn app.main:app --reload
```
### Use Cases
To calculate remaining cash after all the bills  
To manage shared expenses

### Assumptions
Monthly income is fixed  
Fixed costs (rent, subscriptions, utilities)

### Caveats
No user authentication  
Does not account for - Emergency funds , Long-term savings goals

# API example

## Get User Groups

**Endpoint**
GET /users/{user_id}/groups

**Description**
Returns all groups associated with a given user.

### Path Parameters

| Name     | Type    | Required | Description        |
|----------|---------|----------|--------------------|
| user_id  | integer | Yes      | ID of the user     |

### Example Request
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/1/groups' \
  -H 'accept: application/json'
```
### Example Successful Response (200 OK)
```bash
{
  "1": {
    "group_id": 1,
    "user_id": 1,
    "group_name": "group of user 1",
    "description": "string",
    "cost": 3,
    "list_of_bills": [
      1,
      2
    ],
    "created_at": "2026-02-04T10:45:56.231Z",
    "updated_at": "2026-02-04T10:45:56.231Z"
  }
}
```






