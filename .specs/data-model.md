

# Data Model: High-Level Structure

This section describes the main data structure of the project, based on the actual Python models found in app/models.

## User Model

- **id**: UUID, primary key, unique identifier for the user
- **username**: string, unique, required
- **password**: string, required
- **firstname**: string, required
- **lastname**: string, required
- **role**: enum (admin, user, guest), required, default is guest

### Relationships
Currently, the User model is standalone, with no direct relationships to other models.

## General Considerations
- User data is managed through the User model, which includes fields for authentication and basic account information.
- The structure can be extended to include relationships with other models (e.g., IoT devices, logs, etc.).
- Roles are managed via an enum field.

## Future Extensions
- Possible addition of models for devices, access logs, dashboard, etc.
- Relationships between users and devices or other system objects.

---
*This description is based on the actual fields found in app/models/user.py. For details on fields and relationships, refer directly to the source files.*
