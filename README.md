# p1-auth

Provides an authentication system for Platform One by decoding non-encrypted JWTs.

Additionally provides configurations to automatically populate user attributes and assign user membership from JWT fields.

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