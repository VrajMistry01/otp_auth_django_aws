from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import random
import string
from .models import OTP


# Generate OTP function
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    print("Generated OTP:", otp)  # Debug: OTP generated
    return otp


# Send OTP email
def send_otp_email(user_email, otp):
    subject = 'Your OTP Code'
    message = f'''
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f7fa;
                color: #333333;
                padding: 20px;
            }}
            .email-container {{
                background-color: #ffffff;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 600px;
                margin: auto;
            }}
            h2 {{
                color: #2a9d8f;
                font-size: 24px;
            }}
            .otp-box {{
                display: inline-block;
                background-color: #2a9d8f;
                color: #ffffff;
                padding: 15px 30px;
                border-radius: 5px;
                font-size: 20px;
                margin-top: 15px;
            }}
            p {{
                font-size: 16px;
            }}
            .footer {{
                margin-top: 25px;
                text-align: center;
                color: #888888;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <h2>Welcome!</h2>
            <p>We received a request to send you a One-Time Password (OTP). Please use the OTP below to proceed with your request.</p>
            <div class="otp-box">
                {otp}
            </div>
            <p>If you did not request this OTP, please ignore this email.</p>
            <div class="footer">
                <p>Thank you for using our service!</p>
                <p>Best regards,<br>The OTP Service Team</p>
            </div>
        </div>
    </body>
    </html>
    '''

    # Send the email with HTML content
    send_mail(
        subject,
        message,
        'noreply@otp.com',
        [user_email],
        fail_silently=False,
        html_message=message,
    )

    print("OTP email sent successfully.")  # Debug: Email sent

# register view


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Input validation
        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'register.html')

        try:
            # Create the user
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.is_active = False  # Deactivate account until verified
            user.save()

            # Generate OTP
            otp = generate_otp()

            # Save OTP in the database
            otp_obj = OTP.objects.create(
                user=user, otp=otp, created_at=timezone.now())
            otp_obj.save()

            # Send OTP email
            send_otp_email(email, otp)

            messages.success(
                request, "Account created successfully! Please verify your email.")
            return redirect('otp_verify', user_id=user.id)

        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return render(request, 'register.html')

    return render(request, 'register.html')

# Login View


def login_view(request):
    print("Login view called")  # Debug: Function entered
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Username entered:", username)  # Debug: Username input
        print("Password entered:", password)  # Debug: Password input

        try:
            # Retrieve the user using get_object_or_404
            user = get_object_or_404(User, username=username)
            print("User fetched from database:", user)  # Debug: User fetched

            # Manually check the password (hashed password comparison)
            print("Fetched fro DB:", user.password)
            if (password == user.password):
                # Debug: Password match
                print(f"Password matched for user: {user.username}")

                # Generate OTP
                otp = generate_otp()

                # Save OTP to database
                otp_obj = OTP.objects.create(
                    user=user, otp=otp, created_at=timezone.now())
                otp_obj.save()
                print("OTP saved to database:", otp)  # Debug: OTP saved

                # Send OTP email
                send_otp_email(user.email, otp)

                # Redirect to OTP verification page
                print("Redirecting to OTP verification page")  # Debug: Redirect
                return redirect('otp_verify', user_id=user.id)
            else:
                # Debug: Password mismatch
                print(f"Password mismatch for user: {username}")
                messages.error(request, 'Invalid username or password')
                return render(request, 'login.html')

        except User.DoesNotExist:
            # Debug: User not found
            print(f"User '{username}' does not exist.")
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

    print("Rendering login page")  # Debug: Initial render
    return render(request, 'login.html')

# OTP Verification View


def otp_verify(request, user_id):
    print("OTP verification view called")  # Debug: Function entered
    user = get_object_or_404(User, id=user_id)
    print("User fetched for OTP verification:", user)  # Debug: User fetched

    if request.method == "POST":
        otp_input = request.POST.get("otp")
        print("OTP entered by user:", otp_input)  # Debug: OTP input

        try:
            # Get the latest OTP for the user
            otp_obj = OTP.objects.filter(user=user).latest('created_at')
            print("Latest OTP fetched from database:",
                  otp_obj.otp)  # Debug: OTP fetched

            # Check if OTP is valid and not expired
            if otp_obj.otp == otp_input:
                elapsed_time = (timezone.now() - otp_obj.created_at).seconds
                print("Time elapsed since OTP creation (seconds):",
                      elapsed_time)  # Debug: Elapsed time

                if elapsed_time <= 300:  # OTP is valid for 5 minutes
                    print("OTP verified successfully for user:",
                          user.username)  # Debug: OTP valid
                    login(request, user)  # Log the user in
                    return redirect('welcome')  # Redirect to a welcome page
                else:
                    # Debug: OTP expired
                    print("OTP expired for user:", user.username)
                    messages.error(
                        request, 'OTP has expired. Please log in again.')
            else:
                print("Invalid OTP entered by user:",
                      otp_input)  # Debug: OTP mismatch
                messages.error(request, 'Invalid OTP. Please try again.')
        except OTP.DoesNotExist:
            # Debug: OTP not found
            print("No OTP found for user:", user.username)
            messages.error(request, 'No OTP found. Please request a new OTP.')

    return render(request, 'otp_verify.html', {'user': user})


# Welcome View (After Successful Login)
def welcome(request):
    print()
    return render(request, 'welcome.html', {'username': request.user.user})
