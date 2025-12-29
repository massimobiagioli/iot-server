
# Use Case Specification: User Login

## 1. Overview
**ID:** UC-001  
**Title:** User Authentication  
**Description:** Allows a registered user to access the platform using their username and password credentials.

---

## 2. Context & Project Reference
- **Project Structure:** See `project-structure.md` for folder hierarchy and architectural patterns.
- **Data Model:** See `data-model.md` for user schema and relationships.
- **Target Components:**  
    - UI: Login Form (`/auth/login`)
    - API: Authentication endpoints (`/auth/do_login`)

---

## 3. Data Schema (Input/Output)

### Input Data
| Field         | Type    | Validation                        |
|---------------|---------|-----------------------------------|
| `username`    | String  | Required, must be a valid username|
| `password`    | String  | Required, minimum 8 characters    |
| `remember_me` | Boolean | Optional (default: false)         |

### Output / Side Effects
| Event                | Action                                                                 |
|----------------------|-----------------------------------------------------------------------|
| **Success (200 OK)** | Set a cookie with user id (`sid`). If `remember_me` is true, set long expiration; otherwise, session cookie. Redirect to `/`. |
| **Failure (401/403)**| Show error message "Invalid credentials" on login page.               |
| **User Not Found**   | Show error message "User not found" on login page.                    |
| **Network Error**    | Show error message "Connection error, please try again later".        |

---

## 4. Functional Workflow

1. **Entry Point:** User navigates to `/auth/login`.
2. **Auth Check:**  
     - If a valid session cookie (`sid`) exists and matches a user, redirect to `/dashboard`.
     - If not, render the login page.
3. **User Action:** User submits credentials via `/auth/do_login` (POST).
4. **Server-Side Validation:**  
     - Validate credentials using the `GetUser` service.
     - On success, set cookie `sid` with user id. If `remember_me` is checked, set a long expiration; otherwise, use a session cookie.
     - On failure, return error and re-render login page with message.
5. **Redirect:**  
     - On successful login, redirect to `/` (which will further redirect to `/dashboard` if authenticated).
     - On error, stay on login page and show error.

---

## 5. Constraints & Business Rules
- **Security:**  
    - Passwords are never stored or logged in plain text.
    - Session management is handled via secure HTTP-only cookies.
- **UI/UX:**  
    - The submit button is disabled if the form is invalid or a request is pending.
    - Error messages are shown inline on the login page.
- **Persistence:**  
    - If `remember_me` is checked, the session persists across browser restarts.
    - Otherwise, session expires when browser is closed.
- **Coding Standard:**  
    - Use strict types for all input/output.
    - Keep UI, business logic, and service layers separated as per project structure.

---

## 6. Implementation Notes
- The authentication flow relies on a FastAPI middleware to set `request.state.current_user` based on the `sid` cookie.
- The login route sets the cookie and redirects; if `remember_me` is not set, the cookie is a session cookie.
- The dashboard and other protected routes read `request.state.current_user` to determine authentication status.
- All error handling and redirects are managed server-side, with clear feedback to the user.