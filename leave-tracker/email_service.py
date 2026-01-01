"""
Email Notification Service
Sends email notifications for leave requests using Outlook SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# SMTP Configuration
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
SMTP_USER = 'ObeidH@adx.ae'
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')  # Set via environment variable

# Scrum Masters (recipients for all notifications)
SCRUM_MASTERS = [
    'ObeidH@adx.ae',  # Husam Alhwadi
    'MurmyloP@adx.ae'  # Peter Murmylo
]


def send_email(to_emails, subject, body_html):
    """
    Send email via Outlook SMTP
    
    Args:
        to_emails: List of recipient emails or single email string
        subject: Email subject
        body_html: HTML body content
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if isinstance(to_emails, str):
        to_emails = [to_emails]
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP_USER
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        
        # Add HTML body
        html_part = MIMEText(body_html, 'html')
        msg.attach(html_part)
        
        # Connect and send
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"✓ Email sent to {', '.join(to_emails)}: {subject}")
        return True
        
    except Exception as e:
        print(f"✗ Email sending failed: {str(e)}")
        return False


def notify_new_leave_request(employee_name, employee_email, stream, leave_type, 
                             start_date, end_date, working_days, reason, request_id):
    """
    Notify Scrum Masters about new leave request
    """
    subject = f"🔔 New Leave Request - {employee_name}"
    
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .detail {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #555; }}
            .button {{ display: inline-block; padding: 10px 20px; margin: 10px 5px; text-decoration: none; 
                      border-radius: 5px; font-weight: bold; }}
            .approve {{ background-color: #4CAF50; color: white; }}
            .reject {{ background-color: #f44336; color: white; }}
            .footer {{ text-align: center; color: #777; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>📋 New Leave Request Submitted</h2>
            </div>
            
            <div class="content">
                <div class="detail">
                    <span class="label">Employee:</span> {employee_name} ({employee_email})
                </div>
                <div class="detail">
                    <span class="label">Stream:</span> {stream}
                </div>
                <div class="detail">
                    <span class="label">Leave Type:</span> {leave_type}
                </div>
                <div class="detail">
                    <span class="label">Period:</span> {start_date} to {end_date}
                </div>
                <div class="detail">
                    <span class="label">Working Days:</span> {working_days} days
                </div>
                {f'<div class="detail"><span class="label">Reason:</span> {reason}</div>' if reason else ''}
            </div>
            
            <div style="text-align: center; margin: 20px 0;">
                <p><strong>Action Required:</strong> Please review and approve/reject this leave request in the admin panel.</p>
            </div>
            
            <div class="footer">
                <p>This is an automated notification from the Leave Tracker System</p>
                <p>Request ID: #{request_id}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(SCRUM_MASTERS, subject, body)


def notify_leave_approved(employee_email, employee_name, leave_type, start_date, 
                         end_date, working_days, remaining_balance):
    """
    Notify employee that their leave request has been approved
    """
    subject = f"✅ Leave Request Approved - {start_date} to {end_date}"
    
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .detail {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #555; }}
            .success {{ color: #4CAF50; font-weight: bold; }}
            .footer {{ text-align: center; color: #777; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>✅ Leave Request Approved</h2>
            </div>
            
            <div class="content">
                <p class="success">Good news {employee_name}! Your leave request has been approved.</p>
                
                <div class="detail">
                    <span class="label">Leave Type:</span> {leave_type}
                </div>
                <div class="detail">
                    <span class="label">Period:</span> {start_date} to {end_date}
                </div>
                <div class="detail">
                    <span class="label">Duration:</span> {working_days} working days
                </div>
                <div class="detail">
                    <span class="label">Remaining Balance:</span> {remaining_balance} days
                </div>
            </div>
            
            <div class="footer">
                <p>Enjoy your time off! 🌴</p>
                <p>This is an automated notification from the Leave Tracker System</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email([employee_email], subject, body)


def notify_leave_rejected(employee_email, employee_name, leave_type, start_date, 
                         end_date, rejection_reason=None):
    """
    Notify employee and Scrum Masters that leave request has been rejected
    """
    subject = f"❌ Leave Request Not Approved - {start_date} to {end_date}"
    
    reason_text = f"<p><strong>Reason:</strong> {rejection_reason}</p>" if rejection_reason else ""
    
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #f44336; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .detail {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #555; }}
            .footer {{ text-align: center; color: #777; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Leave Request Update</h2>
            </div>
            
            <div class="content">
                <p>Dear {employee_name},</p>
                <p>Unfortunately, your leave request could not be approved at this time.</p>
                
                <div class="detail">
                    <span class="label">Leave Type:</span> {leave_type}
                </div>
                <div class="detail">
                    <span class="label">Requested Period:</span> {start_date} to {end_date}
                </div>
                
                {reason_text}
                
                <p>If you have questions or would like to discuss alternative dates, please contact your Scrum Master.</p>
            </div>
            
            <div class="footer">
                <p>This is an automated notification from the Leave Tracker System</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send to employee and Scrum Masters
    recipients = [employee_email] + SCRUM_MASTERS
    return send_email(recipients, subject, body)


def notify_overlap_blocked(employee_email, employee_name, overlapping_employee, 
                          overlapping_dates, start_date, end_date):
    """
    Notify employee that their leave request was blocked due to overlap
    """
    subject = f"⚠️ Leave Request Blocked - Overlapping Vacation"
    
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #FF9800; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .detail {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #555; }}
            .warning {{ background-color: #fff3cd; padding: 10px; border-left: 4px solid #FF9800; margin: 15px 0; }}
            .footer {{ text-align: center; color: #777; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>⚠️ Leave Request Cannot Be Submitted</h2>
            </div>
            
            <div class="content">
                <p>Dear {employee_name},</p>
                <p>Your leave request could not be submitted due to an overlapping vacation in your stream.</p>
                
                <div class="warning">
                    <strong>Policy:</strong> Only one team member per stream can be on leave at the same time.
                </div>
                
                <div class="detail">
                    <span class="label">Your Requested Dates:</span> {start_date} to {end_date}
                </div>
                <div class="detail">
                    <span class="label">Conflict With:</span> {overlapping_employee}
                </div>
                <div class="detail">
                    <span class="label">Their Leave Dates:</span> {overlapping_dates[0]} to {overlapping_dates[1]}
                </div>
                
                <p><strong>Next Steps:</strong></p>
                <ul>
                    <li>Coordinate with your team member</li>
                    <li>Choose different dates</li>
                    <li>Or contact your Scrum Master for special approval</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>This is an automated notification from the Leave Tracker System</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email([employee_email], subject, body)


def notify_insufficient_balance(employee_email, employee_name, leave_type, 
                               requested_days, current_balance, shortfall):
    """
    Notify employee that their leave request was blocked due to insufficient balance
    """
    subject = f"⚠️ Leave Request Blocked - Insufficient Balance"
    
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #f44336; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .detail {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #555; }}
            .error {{ color: #f44336; font-weight: bold; }}
            .footer {{ text-align: center; color: #777; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>⚠️ Insufficient {leave_type} Leave Balance</h2>
            </div>
            
            <div class="content">
                <p>Dear {employee_name},</p>
                <p>Your leave request could not be submitted due to insufficient balance.</p>
                
                <div class="detail">
                    <span class="label">Leave Type:</span> {leave_type}
                </div>
                <div class="detail">
                    <span class="label">Requested Days:</span> {requested_days} days
                </div>
                <div class="detail">
                    <span class="label">Your Current Balance:</span> {current_balance} days
                </div>
                <div class="detail">
                    <span class="label error">Shortfall:</span> {shortfall} days
                </div>
                
                <p><strong>Options:</strong></p>
                <ul>
                    <li>Reduce the number of leave days</li>
                    <li>Contact HR to discuss your leave balance</li>
                    <li>Contact your Scrum Master for special approval</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>This is an automated notification from the Leave Tracker System</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email([employee_email], subject, body)


def notify_manager_override(employee_name, employee_email, override_reason, 
                           leave_details, approved_by_name):
    """
    Notify when manager uses override to approve exceptional leave
    """
    subject = f"🔓 Manager Override Used - {employee_name} Leave Approved"
    
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #FF9800; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .detail {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #555; }}
            .override {{ background-color: #fff3cd; padding: 15px; border-left: 4px solid #FF9800; margin: 15px 0; }}
            .footer {{ text-align: center; color: #777; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🔓 Manager Override Notification</h2>
            </div>
            
            <div class="content">
                <div class="override">
                    <strong>⚠️ Override Used:</strong> This leave request was approved with manager override, 
                    bypassing standard validation rules.
                </div>
                
                <div class="detail">
                    <span class="label">Employee:</span> {employee_name} ({employee_email})
                </div>
                <div class="detail">
                    <span class="label">Approved By:</span> {approved_by_name}
                </div>
                <div class="detail">
                    <span class="label">Leave Details:</span> {leave_details}
                </div>
                <div class="detail">
                    <span class="label">Override Reason:</span> {override_reason}
                </div>
            </div>
            
            <div class="footer">
                <p>This is an automated notification to all Scrum Masters</p>
                <p>Leave Tracker System</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send to both employee and Scrum Masters
    recipients = [employee_email] + SCRUM_MASTERS
    return send_email(recipients, subject, body)


# Test function
if __name__ == '__main__':
    print("Email Service Configuration:")
    print(f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"From: {SMTP_USER}")
    print(f"Scrum Masters: {', '.join(SCRUM_MASTERS)}")
    print("\nTo test, set SMTP_PASSWORD environment variable and run a notification function")
