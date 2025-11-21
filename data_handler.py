import sqlite3
from datetime import datetime

class DataHandler:
    def __init__(self):
        self.student_db = "students.db"
        self.log_db = "logger.db"
        
        # Nigerian banks list
        self.valid_banks = [
            "Access Bank", "GTBank", "First Bank", "UBA", "Zenith Bank",
            "Fidelity Bank", "Union Bank", "Sterling Bank", "Stanbic IBTC",
            "Ecobank", "FCMB", "Wema Bank", "Polaris Bank", "Keystone Bank",
            "Unity Bank", "Providus Bank", "Jaiz Bank", "Opay", "Palmpay", "Kuda"
        ]
        
        # Configuration
        self.MIN_PRICE = 100
        self.MAX_PRICE = 10000
        self.CAFETERIA_OPEN = 6  # 6 AM
        self.CAFETERIA_CLOSE = 23  # 11 PM
        self.MAX_DAILY_TRANSACTIONS = 3
        self.RAPID_PURCHASE_MINUTES = 10
    
    def validate_matric(self, matric):
        """Check if matric number exists in student database"""
        try:
            conn = sqlite3.connect(self.student_db)
            c = conn.cursor()
            c.execute("SELECT name, department FROM students WHERE matric=?", (matric.strip(),))
            result = c.fetchone()
            conn.close()
            
            if result:
                return True, result[0], result[1]  # Returns: (True, name, department)
            else:
                return False, None, None
        except Exception as e:
            print(f"Error validating matric: {e}")
            return False, None, None
    
    def validate_price(self, price):
        """Check if price is within valid range"""
        try:
            price = int(price)
            if self.MIN_PRICE <= price <= self.MAX_PRICE:
                return True, price, None
            else:
                return False, None, f"Price must be between ₦{self.MIN_PRICE} and ₦{self.MAX_PRICE}"
        except ValueError:
            return False, None, "Price must be a valid number"
    
    def validate_bank(self, bank_name):
        """Check if bank is in approved list"""
        if bank_name in self.valid_banks:
            return True, None
        else:
            return False, f"Invalid bank. Please select from the list"
    
    def check_time_window(self):
        """Check if current time is within cafeteria hours"""
        current_hour = datetime.now().hour
        if self.CAFETERIA_OPEN <= current_hour <= self.CAFETERIA_CLOSE:
            return True, None
        else:
            return False, f"Cafeteria is closed. Operating hours: {self.CAFETERIA_OPEN}AM - {self.CAFETERIA_CLOSE}PM"
    
    def check_duplicate_recent(self, matric):
        """Check if student made purchase in last 10 minutes"""
        try:
            conn = sqlite3.connect(self.log_db)
            c = conn.cursor()
            
            # Get last transaction time for this student
            c.execute("""SELECT timestamp FROM log 
                        WHERE matric=? 
                        ORDER BY timestamp DESC LIMIT 1""", (matric,))
            result = c.fetchone()
            conn.close()
            
            if result:
                last_time = datetime.fromisoformat(result[0])
                time_diff = (datetime.now() - last_time).total_seconds() / 60
                
                if time_diff < self.RAPID_PURCHASE_MINUTES:
                    return True, f"Rapid purchase detected! Last purchase was {int(time_diff)} minutes ago"
            
            return False, None
        except Exception as e:
            print(f"Error checking duplicates: {e}")
            return False, None
    
    def check_daily_limit(self, matric):
        """Check if student exceeded daily transaction limit"""
        try:
            conn = sqlite3.connect(self.log_db)
            c = conn.cursor()
            
            today = datetime.now().date().isoformat()
            c.execute("""SELECT COUNT(*) FROM log 
                        WHERE matric=? AND DATE(timestamp)=?""", (matric, today))
            count = c.fetchone()[0]
            conn.close()
            
            if count >= self.MAX_DAILY_TRANSACTIONS:
                return True, f"Daily limit reached! Maximum {self.MAX_DAILY_TRANSACTIONS} transactions per day"
            
            return False, None
        except Exception as e:
            print(f"Error checking daily limit: {e}")
            return False, None
    
    def generate_flags(self, matric, price):
        """Generate warning flags for suspicious transactions"""
        flags = []
        
        # Check for high amount
        if price > 5000:
            flags.append("HIGH_AMOUNT")
        
        # Check for rapid purchase
        is_rapid, msg = self.check_duplicate_recent(matric)
        if is_rapid:
            flags.append("RAPID_PURCHASE")
        
        # Check daily limit
        at_limit, msg = self.check_daily_limit(matric)
        if at_limit:
            flags.append("DAILY_LIMIT_REACHED")
        
        # Check time
        valid_time, msg = self.check_time_window()
        if not valid_time:
            flags.append("OFF_HOURS")
        
        return ",".join(flags) if flags else ""
    
    def get_timestamp(self):
        """Get current timestamp"""
        return datetime.now().isoformat()