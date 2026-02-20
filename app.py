from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'campus-mart-secret-key-2024'

# Sample user database (in real app, use proper database)
users = {
    'admin': {'password': 'admin123', 'email': 'admin@campusmart.com'},
    'student': {'password': 'student123', 'email': 'student@college.com'}
}

# All products data
all_products = [
    {'id': 1, 'name': 'Ballpoint Pens (Pack of 10)', 'price': 40, 'category': 'Writing Tools', 'description': 'Smooth blue and black ballpoint pens'},
    {'id': 2, 'name': 'Gel Pens (Pack of 12)', 'price': 60, 'category': 'Writing Tools', 'description': '12 vibrant colors gel pens'},
    {'id': 3, 'name': 'Fountain Pen', 'price': 150, 'category': 'Writing Tools', 'description': 'Classic fountain pen with ink'},
    {'id': 4, 'name': 'HB Pencils (Pack of 10)', 'price': 30, 'category': 'Writing Tools', 'description': 'Standard HB pencils for writing'},
    {'id': 5, 'name': 'Mechanical Pencils (Pack of 5)', 'price': 80, 'category': 'Writing Tools', 'description': '0.5mm mechanical pencils with eraser'},
    {'id': 6, 'name': 'Colored Pencils (24 colors)', 'price': 120, 'category': 'Writing Tools', 'description': '24 assorted color pencils'},
    {'id': 7, 'name': 'Highlighters (Pack of 6)', 'price': 50, 'category': 'Writing Tools', 'description': '6 fluorescent highlighters'},
    {'id': 8, 'name': 'Whiteboard Markers (4 colors)', 'price': 70, 'category': 'Writing Tools', 'description': 'Red, blue, black, green markers'},
    {'id': 9, 'name': 'College Notebooks (200 pages)', 'price': 80, 'category': 'Paper Products', 'description': 'Single line ruled notebooks'},
    {'id': 10, 'name': 'Spiral Notebooks (150 pages)', 'price': 90, 'category': 'Paper Products', 'description': 'Spiral bound multi-subject notebooks'},
    {'id': 11, 'name': 'Sticky Notes (5 pads)', 'price': 45, 'category': 'Paper Products', 'description': 'Assorted color sticky notes'},
    {'id': 12, 'name': 'Student Diary/Planner', 'price': 120, 'category': 'Paper Products', 'description': 'Academic year planner with calendar'},
    {'id': 13, 'name': 'A4 Printer Paper (500 sheets)', 'price': 200, 'category': 'Paper Products', 'description': 'Premium quality printer paper'},
    {'id': 14, 'name': 'Graph Sheets (100 sheets)', 'price': 40, 'category': 'Paper Products', 'description': '5x5 graph paper for engineering'},
    {'id': 15, 'name': 'Geometry Box Set', 'price': 150, 'category': 'Desk Supplies', 'description': 'Compass, protractor, ruler, set squares'},
    {'id': 16, 'name': '12-inch Ruler', 'price': 15, 'category': 'Desk Supplies', 'description': 'Plastic transparent ruler'},
    {'id': 17, 'name': 'Eraser (Pack of 5)', 'price': 20, 'category': 'Desk Supplies', 'description': 'Soft white erasers'},
    {'id': 18, 'name': 'Pencil Sharpener', 'price': 15, 'category': 'Desk Supplies', 'description': 'Metal blade sharpener with container'},
    {'id': 19, 'name': 'Scissors', 'price': 35, 'category': 'Desk Supplies', 'description': 'Student scissors 6 inch'},
    {'id': 20, 'name': 'Paper Cutter', 'price': 50, 'category': 'Desk Supplies', 'description': 'Safety paper cutter'},
    {'id': 21, 'name': 'Glue Stick', 'price': 25, 'category': 'Desk Supplies', 'description': 'Non-toxic glue stick'},
    {'id': 22, 'name': 'Transparent Tape', 'price': 30, 'category': 'Desk Supplies', 'description': 'Clear adhesive tape with dispenser'},
    {'id': 23, 'name': 'File Folders (Pack of 10)', 'price': 60, 'category': 'Organization', 'description': 'Assorted color file folders'},
    {'id': 24, 'name': 'Plastic Files (Pack of 5)', 'price': 80, 'category': 'Organization', 'description': 'Transparent plastic files'},
    {'id': 25, 'name': 'Paper Clips (Box of 100)', 'price': 20, 'category': 'Organization', 'description': 'Assorted size paper clips'},
    {'id': 26, 'name': 'Binder Clips (Pack of 12)', 'price': 35, 'category': 'Organization', 'description': 'Mixed size binder clips'},
    {'id': 27, 'name': 'Push Pins (Box of 50)', 'price': 25, 'category': 'Organization', 'description': 'Colorful push pins'},
    {'id': 28, 'name': 'Envelopes (Pack of 20)', 'price': 40, 'category': 'Organization', 'description': 'White business envelopes'},
    {'id': 29, 'name': 'Stapler', 'price': 70, 'category': 'Organization', 'description': 'Desktop stapler'},
    {'id': 30, 'name': 'Staples (Box of 1000)', 'price': 25, 'category': 'Organization', 'description': 'Standard size staples'},
    {'id': 31, 'name': 'Sketch Pens (50 colors)', 'price': 180, 'category': 'Creative', 'description': '50 colors sketch pen set'},
    {'id': 32, 'name': 'Crayons (24 colors)', 'price': 90, 'category': 'Creative', 'description': 'Wax crayons for drawing'},
    {'id': 33, 'name': 'Watercolor Set (12 colors)', 'price': 150, 'category': 'Creative', 'description': 'Watercolor paints with brush'},
    {'id': 34, 'name': 'Paint Brushes (Set of 5)', 'price': 80, 'category': 'Creative', 'description': 'Different size paint brushes'},
    {'id': 35, 'name': 'Craft Paper (50 sheets)', 'price': 120, 'category': 'Creative', 'description': 'Assorted color craft paper'},
    {'id': 36, 'name': 'Origami Sheets (100 sheets)', 'price': 60, 'category': 'Creative', 'description': 'Colorful origami paper'},
]

# AI Agent Class
class CampusMartAIAgent:
    def __init__(self):
        pass
    
    def process_message(self, message):
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! Welcome to Campus Mart! 🤖 How can I help you with campus supplies today?"
        
        elif any(word in message_lower for word in ['thank', 'thanks']):
            return "You're welcome! 😊 Let me know if you need anything else."
        
        elif any(word in message_lower for word in ['pen', 'pens']):
            return self.get_ai_recommendations("pens")
        
        elif any(word in message_lower for word in ['notebook', 'book']):
            return self.get_ai_recommendations("notebooks")
        
        elif any(word in message_lower for word in ['stationery', 'supplies']):
            return self.get_ai_recommendations("stationery")
        
        elif any(word in message_lower for word in ['price', 'cost']):
            return "I'll check prices for you! Could you specify which product?"
        
        elif any(word in message_lower for word in ['cart', 'buy', 'order']):
            return "You can add items to cart from our products page! Need recommendations first?"
        
        else:
            return self.get_ai_recommendations(message)
    
    def get_ai_recommendations(self, user_request):
        request_lower = user_request.lower()
        matched_products = []
        
        for product in all_products:
            if (request_lower in product['name'].lower() or 
                request_lower in product['category'].lower() or
                request_lower in product['description'].lower()):
                matched_products.append(product)
        
        if not matched_products:
            matched_products = all_products[:6]
        
        response = "🎯 **AI Recommendations:**\n\n"
        for product in matched_products[:4]:  # Show max 4 products
            response += f"• **{product['name']}** - ₹{product['price']}\n"
            response += f"  _{product['description']}_\n\n"
        
        response += "🛒 **Ready to order?** Visit our products page!"
        return response

# Create AI Agent instance
ai_agent = CampusMartAIAgent()

# Initialize cart
@app.before_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = []

# Routes
@app.route('/')
def index():
    featured_products = all_products[:6]  # First 6 products as featured
    return render_template('index.html', products=featured_products)

@app.route('/products')
def products():
    return render_template('products.html', products=all_products)

@app.route('/ai-assistant')
def ai_assistant():
    return render_template('ai_assistant.html')

@app.route('/ai-chat', methods=['POST'])
def ai_chat():
    try:
        user_message = request.json.get('message', '')
        ai_response = ai_agent.process_message(user_message)
        
        return jsonify({
            'success': True,
            'user_message': user_message,
            'ai_response': ai_response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        
        # Validate product exists
        product = next((p for p in all_products if p['id'] == product_id), None)
        if not product:
            return jsonify({'success': False, 'error': 'Product not found'})
        
        if 'cart' not in session:
            session['cart'] = []
        
        # Check if product already in cart
        cart_item = next((item for item in session['cart'] if item['product_id'] == product_id), None)
        
        if cart_item:
            cart_item['quantity'] += 1
        else:
            session['cart'].append({
                'product_id': product_id,
                'quantity': 1
            })
        
        session.modified = True
        
        return jsonify({
            'success': True, 
            'message': 'Product added to cart!',
            'cart_count': len(session['cart'])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_cart_count')
def get_cart_count():
    try:
        cart_count = len(session.get('cart', []))
        return jsonify({'cart_count': cart_count})
    except Exception as e:
        return jsonify({'cart_count': 0})

@app.route('/update_cart_quantity', methods=['POST'])
def update_cart_quantity():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        action = data.get('action')
        
        if 'cart' not in session or not session['cart']:
            return jsonify({'success': False, 'error': 'Cart is empty'})
        
        cart_item = next((item for item in session['cart'] if item['product_id'] == product_id), None)
        
        if cart_item:
            if action == 'increase':
                cart_item['quantity'] += 1
            elif action == 'decrease':
                if cart_item['quantity'] > 1:
                    cart_item['quantity'] -= 1
                else:
                    # Remove item if quantity becomes 0
                    session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]
            
            session.modified = True
            return jsonify({'success': True, 'message': 'Quantity updated'})
        else:
            return jsonify({'success': False, 'error': 'Product not found in cart'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    try:
        if 'cart' in session:
            session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]
            session.modified = True
            flash('Item removed from cart!', 'success')
        return redirect(url_for('cart'))
    except Exception as e:
        flash('Error removing item from cart', 'danger')
        return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    try:
        cart_items = []
        total = 0
        
        if 'cart' in session:
            for cart_item in session['cart']:
                product = next((p for p in all_products if p['id'] == cart_item['product_id']), None)
                if product:
                    item_total = product['price'] * cart_item['quantity']
                    cart_items.append({
                        'product': product,
                        'quantity': cart_item['quantity'],
                        'item_total': item_total
                    })
                    total += item_total
        
        return render_template('cart.html', cart_items=cart_items, total=total)
    except Exception as e:
        flash('Error loading cart', 'danger')
        return render_template('cart.html', cart_items=[], total=0)

# Checkout and Order Routes
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        flash('Please login to checkout!', 'warning')
        return redirect(url_for('login'))
    
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('products'))
    
    # Calculate cart total
    cart_items = []
    total = 0
    
    for cart_item in session['cart']:
        product = next((p for p in all_products if p['id'] == cart_item['product_id']), None)
        if product:
            item_total = product['price'] * cart_item['quantity']
            cart_items.append({
                'product': product,
                'quantity': cart_item['quantity'],
                'item_total': item_total
            })
            total += item_total
    
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        address = request.form.get('address')
        city = request.form.get('city')
        pincode = request.form.get('pincode')
        phone = request.form.get('phone')
        
        # Validate required fields
        if not all([full_name, email, address, city, pincode, phone]):
            flash('Please fill all required fields!', 'danger')
            return render_template('checkout.html', cart_items=cart_items, total=total)
        
        # Process the order
        order_id = f"CM{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Store order details in session (in real app, save to database)
        if 'orders' not in session:
            session['orders'] = []
        
        session['orders'].append({
            'order_id': order_id,
            'items': cart_items,
            'total': total,
            'shipping_info': {
                'full_name': full_name,
                'email': email,
                'address': address,
                'city': city,
                'pincode': pincode,
                'phone': phone
            },
            'order_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Clear the cart after successful order
        session['cart'] = []
        session.modified = True
        
        flash(f'Order placed successfully! Order ID: {order_id}', 'success')
        return redirect(url_for('order_confirmation', order_id=order_id))
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/order-confirmation/<order_id>')
def order_confirmation(order_id):
    if 'user_id' not in session:
        flash('Please login to view orders!', 'warning')
        return redirect(url_for('login'))
    
    return render_template('order_confirmation.html', order_id=order_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check credentials
        if username in users and users[username]['password'] == password:
            session['user_id'] = username
            session['username'] = username
            session['email'] = users[username]['email']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user exists
        if username in users:
            flash('Username already exists!', 'danger')
        else:
            users[username] = {'password': password, 'email': email}
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/test-ai')
def test_ai():
    test_messages = ['hello', 'pens', 'notebooks', 'stationery']
    results = []
    for msg in test_messages:
        response = ai_agent.process_message(msg)
        results.append(f"Input: {msg} -> Output: {response}")
    return "<br>".join(results)

if __name__ == '__main__':
    print("🚀 Campus Mart Backend Started!")
    print("📍 Visit: http://127.0.0.1:5000")
    print("🤖 AI Assistant: http://127.0.0.1:5000/ai-assistant")
    print("🛒 Products: http://127.0.0.1:5000/products")
    print("🛍️ Cart: http://127.0.0.1:5000/cart")
    print("💳 Checkout: http://127.0.0.1:5000/checkout")
    print("🔐 Login: http://127.0.0.1:5000/login (Use: admin/admin123)")
    print("📝 Register: http://127.0.0.1:5000/register")
    app.run(debug=True)