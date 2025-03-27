# p1-auth

Provides an authentication system for Platform One by decoding non-encrypted JWTs.

> [!CAUTION]
> Signatures are not verified.

Additionally provides configurations to automatically populate user attributes and assign user membership from JWT fields.

## Installation

After running `pip install p1-auth` add the following to the settings.py file as needed.

```python
INSTALLED_APPS = [
    ...
    'p1_auth',
    ...
]
```

Adding `p1_auth` to the `INSTALLED_APPS` is required for use.

```python
MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
    'p1_auth.middleware.AuthenticateSessionMiddleware',
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
]
```

The `p1-auth` middleware can be used to force creation of sessions for use with django admin.  If it is used, it should be between django `SessionMiddleware` and `AuthenticationMiddleware` as shown above.

```python
AUTHENTICATION_BACKENDS = (
    ...
    'p1_auth.backends.PlatformOneAuthentication',
    ...
)
```

`PlatformOneAuthentication` authenticates django requests.

```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': [
        ...
        'p1_auth.backends.PlatformOneRestAuthentication',
        ...
    ],
    ...
}
```

`PlatformOneRestAuthentication` authenticates django-rest-framework requests.

## settings.py

This section covers configurations that can be set in the settings.py file.

### USER_ATTRIBUTES_MAP

A python dictionary to map between fields on the User model and the JWT fields.

```python
USER_ATTRIBUTES_MAP = {
    "PYTHON_USER_MODEL_FIELD_NAME": "JWT_FIELD_NAME",
    "first_name": "given_name",
}
```

### USER_MEMBERSHIPS

A python dictionary to map between models based on JWT fields.  The JWT side can be an id, string, or list.

NOTE: the connection between the models must allow connections like the following `user.connection_name.update_or_create(**{"field_name": "jwt_memberships"})`

```python
USER_MEMBERSHIPS = {
    "PYTHON_USER_MODEL_CONNECTION_NAME": {
        "CONNECTED_MODEL_FIELD": "JWT_MEMBERSHIP_FIELD"
    },
    "groups": {
        "name": "simple_groups"
    },
}
```

### USER_STAFF_FLAG

A key for the JWT to be checked to determine if the user should be marked as staff.  This uses the `is_staff` flag Django's AbstractUser model.

NOTE: if USER_STAFF_VALUE is not set, staff status will be determined by USER_STAFF_FLAG existing in the JWT, and having a non-empty value.  So an empty list or string will not confer staff status.

```python
USER_STAFF_FLAG = "JWT_STAFF_FLAG"
```

### USER_STAFF_VALUE

A value to check for in the JWT under the USER_STAFF_FLAG.  If the JWT contains a list under USER_STAFF_FLAG, it will check to see if the value of USER_STAFF_VALUE is within the list.  The value of USER_STAFF_VALUE is not type restricted, but the comparison is type dependent, so `'1' == 1` would fail.

```python
USER_STAFF_VALUE = 123
```

### USER_SUPERUSER_FLAG

A key for the JWT to be checked to determine if the user should be marked as superuser.  This uses the `is_superuser` flag Django's AbstractUser model.

NOTE: if USER_SUPERUSER_VALUE is not set, superuser status will be determined by USER_SUPERUSER_FLAG existing in the JWT, and having a non-empty value.  So an empty list or string will not confer staff status.

```python
USER_SUPERUSER_FLAG = "JWT_SUPERUSER_FLAG"
```

### USER_SUPERUSER_VALUE

A value to check for in the JWT under the USER_SUPERUSER_FLAG.  If the JWT contains a list under USER_SUPERUSER_FLAG, it will check to see if the value of USER_SUPERUSER_VALUE is within the list.  The value of USER_SUPERUSER_VALUE is not type restricted, but the comparison is type dependent, so `'1' == 1` would fail.

```python
USER_SUPERUSER_VALUE = 123
```

### REQUIRE_JWT

A flag to require JWTs on every request.

```python
REQUIRE_JWT = True
```

### JWT_PREFERRED_USERNAME_FIELD

The field to use to populate the Username Field of the Django User model.  This defaults to `preferred_username`.

```python
JWT_PREFERRED_USERNAME_FIELD = "email"
```

### CUSTOM_AUTHENTICATION_LOGIC

> [!CAUTION]
> This gives access to the decoded JWT and the User model, so care should be taken when using this capability as sensitive data will be present.

A list of callables or strings that accepts three parameters `jwt_decoded`, `user`, and `new`.

`jwt_decoded` (dict): The dictionary containing the decoded JWT.

`user` (AbstractBaseUser): The authenticated user object, it is expected to be an AbstractBaseUser, but can be any model.

`new` (bool): A boolean that is true if the user object has been created by this request.

```python
CUSTOM_AUTHENTICATION_LOGIC = [
    some_callable,
    'path.to.some.other.callable',
    'p1_auth.callables.raise_error_if_email_not_validated'
]
```


## Django Admin

This section covers configurations that can be set in the Django Admin.

### RelatedAssignment

RelatedAssignment allows selecting a Model (object_model) and instance (object_pk) that a user should be assigned to if all related AttributeChecks pass.

Object_model is a dropdown of the enabled content types within the application, where you select the object type you want to assign users to.

Object_pk is the Primary Key of the object you want to assign users to.

### AttributeCheck

AttributeCheck allows specifying the JWT key (jwt_attribute) and an expected value.

Jwt_attribute should be a valid JSON key, or a JSON object for traversing the JWT to where the key will be.

Expected_value is the expected JSON value.


## Extending Functionality

This section covers how to easily add custom logic that can't be handled within the Django Admin or settings such as USER_ATTRIBUTE_MAP.

### CUSTOM_AUTHENTICATION_LOGIC

> [!CAUTION]
> This gives access to the decoded JWT and the User model, so care should be taken when using this capability as sensitive data will be present.

As described within the settings section [CUSTOM_AUTHENTICATION_LOGIC](#custom_authentication_logic) allows passing callables with custom logic to be executed while authenticating the user.
Each callable must accept 3 arguments: `jwt_decoded`, `user`, and `new`.

`jwt_decoded` (dict): The dictionary containing the decoded JWT.

`user` (AbstractBaseUser): The authenticated user object, it is expected to be an AbstractBaseUser, but can be any model.

`new` (bool): A boolean that is true if the user object has been created by this request.

Generic callables are included in [callables.py](p1_auth/callables.py) and are described below.

#### raise_error_if_email_not_validated

This callable checks the JWT for `email_verified`, if it does not contain `email_verified` with a value of `True` `PermissionDenied` is raised to fail the request with a `403 Forbidden` response.