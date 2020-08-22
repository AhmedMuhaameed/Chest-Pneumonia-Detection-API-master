## To run project
1. to install requirements run `pip install -r requirements.txt`
2. run `python app.py`

### Routes in project
#### User Routes
1. **POST** `/api/users/register`
> to register new user
2. **POST** `/api/users/login`
> to login by email & password
3. **GET** `/api/user`
> to get current user
4. **GET** `/api/users`
> to get all users registered in system
5. **GET** `/api/users/logout`
> to logout
#### Posts Routes
1. **POST** `/api/posts/new/ray`
> to add new ray; just pass image path
2. **GET** `/api/posts`
> to get all posts in system
3.  **GET** `/api/posts/<int:id>`
> to get posts posted by specific user
4. **DELETE** `/api/posts/<int:id>`
> to delete specific post