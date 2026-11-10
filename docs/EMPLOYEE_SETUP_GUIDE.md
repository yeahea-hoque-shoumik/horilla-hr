# Employee Setup Guide

How to create an employee in Horilla so they can log in, check in/out, and apply for leave.

> **Important:** Horilla creates the login account automatically when you save an employee, but it never emails the password. The admin generates a one-time password and passes it to the employee.

---

## Part A: One-time setup (admin, do this once)

1. **Log in as admin/superuser.**
2. **Company structure.** Go to **Settings** and add your **Company**, **Department**, **Job Position**, **Work Type** and **Employee Shift**. Give the shift its working hours for each day.
3. **Turn on Check-In.** Go to **Settings → Attendance → Check In / Check Out** and switch it **on** for your company. If it's off, employees won't see a working Check-In button.
   - Optional, also in Attendance settings: **IP Login Restriction** and **Geofencing**. If either is enabled, check-in only works from the allowed network or location.
4. **Leave types.** Go to **Leave → Configuration** and create leave types such as Casual or Sick, with the number of days and the reset period.

## Part B: Create the employee

5. Go to **Employee → Employees** and click **Create**.
6. **Personal info:** First Name, **Email** (required and unique, and it becomes the **username**), Phone. Save.
7. **Work info:** on the employee's profile, open the **Work Information** tab and set Company, Department, Job Position, **Shift**, Work Type and **Reporting Manager**.
   - Check-in uses the shift.
   - Leave approval goes to the reporting manager.

When you save, Horilla automatically creates the user account (`employee/models.py`, `Employee.save()`). The username is the email and the password is random.

## Part C: Give the employee a password

8. In **Employee → Employees** (list view), open the row's action buttons and click **Reset Password**. Confirm.
9. A pop-up shows the new password **once**. Copy it and send it to the employee.
   - For many employees at once, select them and use the bulk **Reset Password** action.

## Part D: Give the employee leave

10. Go to **Leave → Leave Balances** and click **Assign**. Pick the leave type(s) and the employee(s), then save. Without this step the employee has no leave to request.

---

## Part E: What the employee does

11. **Log in.** Open the Horilla URL and log in with their **email** and the **one-time password**.
12. **Change password.** They are sent straight to the **Change Password** page and can't use anything else until they set their own password.
13. **Check in / out.** Click the **Check-In** button in the top bar. The same button then becomes **Check-Out**. History is under **Attendance → My Attendances**.
14. **Apply for leave.** Go to **Leave → My Leave Requests** and click **Create**. Pick the leave type and dates, then submit.
15. **Approval.** The reporting manager or HR approves or rejects it in **Leave → Leave Requests**, and the employee sees the status in **My Leave Requests**.

---

## Common problems

| Problem | Cause |
|---|---|
| Check-In does nothing or is missing | Check-In is off in Settings → Attendance, or the employee has no shift / work info |
| "Check-In Restricted: Your current network is not authorized" | IP restriction is on and the employee is outside the allowed IPs |
| No leave types when creating a request | Leave hasn't been assigned (step 10) |
| Employee forgot their password | Admin repeats step 8. The "Forgot password" link on the login page only works if outgoing email (SMTP) is set up |
