from flask import Blueprint, request, redirect, render_template, url_for, flash, get_flashed_messages
from website import db
from website.models import Product

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
def home():

    return render_template("Homepage.html")

@views.route('/profile', methods=['POST', 'GET'])    
def the_profile():

    return render_template("profile.html")

@views.route('/sign_up_user', methods=['POST', 'GET'])
def sign_in():

    return render_template("signup.html")
        
@views.route('/login_user', methods=['POST', 'GET'])
def login():

    return render_template("login.html")

@views.route('/inventory', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST': 
            id = request.form.get('id')
            product_name = request.form.get('product_name')
            price = request.form.get('price')
            stock = request.form.get('stock')
            manufacturer = request.form.get('manufacturer')
            category = request.form.get('category')

            existing_product = Product.query.filter_by(product_name=product_name).first()

            if existing_product:
                flash('Product already exists!.', category='error')
                return redirect('/inventory')
            else:
                new_product = Product(id=id, product_name=product_name, price=price, stock=stock, manufacturer=manufacturer, category=category)

                try:
                    db.session.add(new_product)
                    db.session.commit()
                    flash('Product added successfully!', category='success')
                    return redirect('/inventory')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Failed to add product! error:{e}', category='error')
                    return redirect('/inventory')
                
    else:
        products = Product.query.order_by(Product.date_created).all()
        return render_template("Inventory.html", products=products, format_price=format_price)
        
@views.route('/search', methods=['POST', 'GET'])
def search():
    querry = request.args.get('search', 'Nothing')

    if querry:
        searches = Product.query.filter(
            Product.product_name.ilike(f'%{querry}%') | Product.manufacturer.ilike(f'%{querry}%') | Product.category.ilike(f'%{querry}%')
            ).order_by(Product.id.asc()).limit(100).all()

    else:
        flash('No product found!', category='error')
        searches = Product.query.all()

    return render_template('search.html', searches=searches, format_price=format_price)

def format_price(price):
    return f"₱{float(price):,.2f}"

@views.route('/Terms of Service')
def tos():
    return '<h1>Terms of Service \
Effective Date: [Insert Date]\
\
Welcome to our website and services. These Terms of Service ("Terms") govern your access to and use of our digital products, services, websites, and applications (collectively, the "Service") provided by [Your Company Name] ("we", "our", or "us"). By using our Service, you agree to be legally bound by these Terms, which constitute a legally binding agreement between you and us. If you do not agree to these Terms, you may not use our Service.\
\
1. Eligibility and Account Registration\
To use the Service, you must be at least 18 years of age or the age of majority in your jurisdiction. If you are under this age, you may only use the Service under the supervision of a parent or legal guardian who agrees to be bound by these Terms on your behalf. You are responsible for providing accurate, current, and complete information when creating an account and for maintaining the confidentiality of your login credentials. You agree to notify us immediately if you suspect unauthorized access to your account.\
\
2. User Conduct\
You agree not to use the Service for any illegal, unauthorized, or unethical purpose. Prohibited activities include but are not limited to: hacking or attempting to gain unauthorized access; violating any applicable law or regulation; distributing malware or malicious code; using automated means (bots, scrapers, spiders) to access or collect data; impersonating others or misrepresenting your affiliation; and disrupting or interfering with the security, integrity, or performance of the Service.\
\
3. License and Intellectual Property\
We grant you a limited, non-exclusive, non-transferable, revocable license to use the Service for personal, non-commercial use, in accordance with these Terms. All rights, title, and interest in and to the Service, including all intellectual property rights, are and will remain the exclusive property of [Your Company Name] and its licensors. You may not copy, reproduce, republish, modify, or distribute any content from the Service without our prior written consent.\
\
4. Content and Submissions\
If you upload, submit, or share content via the Service, you grant us a worldwide, royalty-free, sublicensable, and transferable license to use, host, reproduce, modify, adapt, publish, and display such content for the purpose of operating and improving the Service. You represent that you have the necessary rights to grant us this license. We reserve the right to remove content that violates these Terms, infringes on intellectual property rights, or is deemed inappropriate in our sole discretion.\
\
5. Termination\
We may suspend or terminate your access to the Service at any time, with or without cause or notice. Reasons for termination may include violation of these Terms, misuse of the Service, or any conduct we deem harmful to other users, us, or third parties. Upon termination, your right to use the Service will cease immediately. Sections of these Terms that by their nature should survive termination will remain in effect.\
\
6. Disclaimer of Warranties\
The Service is provided “as is” and “as available” without warranties of any kind, whether express or implied. We do not guarantee that the Service will be secure, error-free, or continuously available. To the fullest extent permitted by law, we disclaim all warranties, including but not limited to implied warranties of merchantability, fitness for a particular purpose, and non-infringement.\
\
7. Limitation of Liability\
To the fullest extent permitted by law, we shall not be liable for any direct, indirect, incidental, special, consequential, or punitive damages resulting from your access to or use of, or inability to access or use, the Service. This includes but is not limited to damages for loss of profits, goodwill, data, or other intangible losses, even if we have been advised of the possibility of such damages.\
\
8. Indemnification\
You agree to indemnify, defend, and hold harmless [Your Company Name] and its affiliates, employees, agents, and licensors from any claims, damages, losses, liabilities, costs, or expenses (including legal fees) arising out of or related to your use of the Service, your violation of these Terms, or your violation of any rights of a third party.\
\
9. Modifications to Terms and Service\
We reserve the right to update or modify these Terms at any time. When changes are made, we will revise the "Effective Date" at the top of the page. Your continued use of the Service after changes are posted constitutes your acceptance of the updated Terms. We also reserve the right to modify or discontinue the Service (or any part thereof) without notice.\
\
10. Governing Law and Jurisdiction\
These Terms shall be governed by and construed in accordance with the laws of the jurisdiction where [Your Company Name] is located, without regard to conflict of law principles. Any legal action or proceeding shall be brought exclusively in the courts of that jurisdiction.\
\
11. Entire Agreement and Severability\
These Terms constitute the entire agreement between you and us regarding the Service and supersede any prior agreements. If any provision is held to be unenforceable, the remaining provisions will continue in full force and effect</h1>'

@views.route('/Privacy Policy')
def privacy():
    return '<h1>Privacy Policy\
Effective Date: [Insert Date]\
\
[Your Company Name] ("we", "our", or "us") values your privacy and is committed to protecting your personal information. This Privacy Policy explains how we collect, use, share, and safeguard your information when you use our services, including any website, application, or feature provided by us (collectively, the "Service"). By using our Service, you consent to the practices described in this policy.\
\
1. Information We Collect\
We collect personal information that you voluntarily provide to us when you register for an account, fill out a form, subscribe to a newsletter, or otherwise interact with our Service. This may include your name, email address, phone number, billing information, and other identifiers. We may also automatically collect certain technical information such as your IP address, browser type, operating system, device identifiers, and usage data through cookies and similar technologies.\
\
2. How We Use Your Information\
We use the information we collect to operate and maintain our Service, provide customer support, process transactions, send administrative and promotional communications, personalize user experiences, monitor usage trends, detect and prevent fraud, enforce our Terms of Service, and comply with legal obligations.\
\
3. Cookies and Tracking Technologies\
We use cookies, web beacons, pixels, and other tracking technologies to enhance your experience, analyze site traffic, and serve relevant content or advertisements. You can modify your browser settings to decline cookies, but some features of the Service may not function properly without them.\
\
4. Sharing of Information\
We may share your information with third-party service providers that perform services on our behalf, such as hosting, data analysis, payment processing, and marketing assistance. These third parties are required to maintain the confidentiality and security of your data. We may also disclose your information in response to lawful requests by public authorities or when required to comply with legal obligations, protect our rights, or prevent harm.\
\
5. Third-Party Services and Links\
Our Service may contain links to third-party websites or services that are not operated or controlled by us. We are not responsible for the privacy practices or content of such third parties, and we encourage you to review their privacy policies before providing them with any personal data.\
\
6. Data Security\
We implement reasonable technical and organizational measures to protect your personal information from unauthorized access, disclosure, alteration, or destruction. However, no method of transmission or storage is 100% secure, and we cannot guarantee absolute security.\
\
7. Data Retention\
We retain your personal information for as long as necessary to fulfill the purposes for which it was collected, including to comply with legal, regulatory, tax, accounting, or reporting requirements. When data is no longer needed, we will securely delete or anonymize it.\
\
8. Your Rights and Choices\
Depending on your location and applicable laws, you may have the right to access, update, correct, or delete your personal information. You may also object to or restrict certain processing activities, withdraw consent at any time, and opt out of receiving promotional communications by following the unsubscribe instructions in our emails.\
\
9. International Data Transfers\
If you access our Service from outside the country where our servers are located, your information may be transferred to, stored, and processed in a country that may not have the same data protection laws as your jurisdiction. By using our Service, you consent to such international transfers of your information.\
\
10. Children’s Privacy\
Our Service is not intended for individuals under the age of 13 (or the equivalent minimum age in your jurisdiction). We do not knowingly collect personal information from children without parental consent. If we learn that we have collected such information, we will delete it promptly.\
\
11. Changes to This Privacy Policy\
We may update this Privacy Policy from time to time to reflect changes in our practices or legal requirements. When we make changes, we will revise the "Effective Date" at the top of this page. Your continued use of the Service following the posting of changes constitutes your acceptance of such changes.\
\
12. Contact Us\
If you have any questions, concerns, or requests related to this Privacy Policy or our data practices, please contact us at:\
Email: privacy@[yourcompany].com\
Address: [Insert Physical Address]</h1>'
