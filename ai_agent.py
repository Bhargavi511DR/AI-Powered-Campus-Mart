import sqlite3
from datetime import datetime

class CampusMartAIAgent:
    def __init__(self, db_path='campus_mart.db'):
        self.db_path = db_path
    
    def process_message(self, message):
        """Main method to process any user message"""
        message_lower = message.lower()
        
        # Basic conversation handling
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! Welcome to Campus Mart! 🤖 How can I help you with campus supplies today?"
        
        elif any(word in message_lower for word in ['thank', 'thanks']):
            return "You're welcome! 😊 Let me know if you need anything else."
        
        elif any(word in message_lower for word in ['bye', 'goodbye']):
            return "Goodbye! 👋 Visit Campus Mart again for all your campus needs!"
        
        elif any(word in message_lower for word in ['help', 'support']):
            return "I can help you: 🔍 Find products, 💰 Check prices, 🛒 Recommend items, 📦 Place orders. What do you need?"
        
        # Product-specific queries
        elif any(word in message_lower for word in ['pen', 'pens']):
            return self.get_ai_recommendations("pens")
        
        elif any(word in message_lower for word in ['notebook', 'book', 'copy']):
            return self.get_ai_recommendations("notebooks")
        
        elif any(word in message_lower for word in ['stationery', 'supplies']):
            return self.get_ai_recommendations("stationery")
        
        elif any(word in message_lower for word in ['price', 'cost', 'how much']):
            return "I'll check prices for you! Could you specify which product you're looking for? Or browse our products page for all prices."
        
        elif any(word in message_lower for word in ['cart', 'buy', 'purchase', 'order']):
            return "You can add items to cart from our products page! Need recommendations first?"
        
        # Complex queries - use AI recommendations
        else:
            return self.get_ai_recommendations(message)
    
    def get_ai_recommendations(self, user_request):
        """
        Generate AI-powered product recommendations based on user request
        """
        try:
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Analyze user request and generate recommendations
            recommendations = self.analyze_request(user_request, cursor)
            
            conn.close()
            
            # Format the response
            return self.format_recommendation_message(recommendations)
            
        except Exception as e:
            return f"I understand you're looking for: '{user_request}'. Currently, I can help you find pens, notebooks, stationery kits, and campus supplies. Could you be more specific?"

    def analyze_request(self, request, cursor):
        """
        Analyze user request and find matching products
        """
        request_lower = request.lower()
        recommendations = {
            'category': '',
            'products': [],
            'total_price': 0,
            'special_offer': '',
            'query_type': 'specific' if len(request_lower.split()) <= 3 else 'complex'
        }
        
        # Define keyword mappings for categories
        categories = {
            'computer': 'Technology',
            'programming': 'Technology', 
            'engineering': 'Engineering',
            'science': 'Science',
            'stationery': 'General',
            'freshman': 'Starter Kit',
            'first year': 'Starter Kit',
            'notes': 'Writing',
            'pen': 'Writing',
            'notebook': 'Writing',
            'pencil': 'Writing',
            'geometry': 'Tools',
            'calculator': 'Technology',
            'drawing': 'Art',
            'art': 'Art',
            'lab': 'Science'
        }
        
        # Determine category
        for keyword, category in categories.items():
            if keyword in request_lower:
                recommendations['category'] = category
                break
        
        # Get relevant products based on category
        if recommendations['category']:
            cursor.execute('''
                SELECT name, price, description, category FROM products 
                WHERE category = ? OR tags LIKE ? OR name LIKE ?
                LIMIT 6
            ''', (recommendations['category'], f'%{recommendations["category"]}%', f'%{request_lower}%'))
        else:
            # Search in product names and descriptions
            cursor.execute('''
                SELECT name, price, description, category FROM products 
                WHERE name LIKE ? OR description LIKE ? OR tags LIKE ?
                LIMIT 6
            ''', (f'%{request_lower}%', f'%{request_lower}%', f'%{request_lower}%'))
        
        products = cursor.fetchall()
        
        # If no products found, get general products
        if not products:
            cursor.execute('SELECT name, price, description, category FROM products LIMIT 6')
            products = cursor.fetchall()
            recommendations['category'] = 'General Campus Supplies'
        
        for product in products:
            recommendations['products'].append({
                'name': product[0],
                'price': product[1],
                'description': product[2],
                'category': product[3]
            })
            recommendations['total_price'] += product[1]
        
        # Generate special offer for kits
        if len(recommendations['products']) >= 3:
            discount = recommendations['total_price'] * 0.1  # 10% discount
            recommendations['special_offer'] = f"Special kit price: ₹{int(recommendations['total_price'] - discount)}!"
        
        return recommendations
    
    def format_recommendation_message(self, recommendations):
        """
        Format recommendations into a readable message
        """
        if not recommendations['products']:
            return "I couldn't find specific products matching your request. 🧐 But we have great campus supplies! Try: 'pens', 'notebooks', or 'stationery kit'."
        
        message = f"🎯 **AI Recommendations for {recommendations['category']}:**\n\n"
        
        for product in recommendations['products']:
            message += f"• **{product['name']}** - ₹{product['price']}\n"
            if product['description']:
                message += f"  _{product['description']}_\n"
        
        if recommendations['special_offer']:
            message += f"\n💰 **{recommendations['special_offer']}**\n"
        elif len(recommendations['products']) > 1:
            message += f"\n💰 **Total: ₹{recommendations['total_price']}**\n"
        
        message += "\n🛒 **Ready to order?** Visit our products page or reply with the items you want!"
        message += "\n\n💡 **Pro Tip:** Say 'add [item] to cart' or ask about specific products!"
        
        return message
    
    def quick_response(self, query_type, product_name=None):
        """Quick responses for common queries"""
        quick_responses = {
            'greeting': "Hello! 👋 I'm your Campus Mart AI assistant. I can help you find products, check prices, and make recommendations. What do you need today?",
            'products': "We have: ✏️ Writing tools, 📒 Notebooks, 📏 Geometry sets, 🎨 Art supplies, 💻 Tech accessories, and more!",
            'delivery': "We offer same-day delivery on campus! 🚀 Orders placed before 3 PM delivered today.",
            'payment': "We accept: 💳 Cards, 📱 UPI, 💵 Cash on Delivery, and college payment methods.",
            'hours': "Campus Mart is available 24/7 online! 🕒 Delivery hours: 9 AM - 7 PM daily."
        }
        return quick_responses.get(query_type, "How can I help you with Campus Mart today?")

# Create global instance
ai_agent = CampusMartAIAgent()

# Utility functions for routes
def process_ai_message(user_input):
    """Main function to process user messages through AI agent"""
    return ai_agent.process_message(user_input)

def get_ai_suggestions(user_input):
    """Get AI product suggestions"""
    return ai_agent.get_ai_recommendations(user_input)

def get_quick_response(query_type):
    """Get quick AI responses"""
    return ai_agent.quick_response(query_type)

# Example usage
if __name__ == "__main__":
    # Test the AI agent
    test_queries = [
        "hello",
        "I need pens for college",
        "notebooks",
        "engineering supplies",
        "what do you have?",
        "thank you"
    ]
    
    for query in test_queries:
        print(f"User: {query}")
        print(f"AI: {process_ai_message(query)}")
        print("-" * 50)