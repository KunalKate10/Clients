import streamlit as st
import hashlib

# Transaction class
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.sender) + str(self.recipient) + str(self.amount)
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

# Block class
class Block:
    def __init__(self, previous_hash, transactions):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.previous_hash) + str([(t.sender, t.recipient, t.amount) for t in self.transactions])
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

# Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("0", [])

    def add_block(self, transactions):
        previous_hash = self.chain[-1].hash
        new_block = Block(previous_hash, transactions)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# Initialize blockchain in session_state
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.title("🧾 Blockchain Invoice Tracker")

st.subheader("Add a New Transaction")

# Input form
with st.form("transaction_form"):
    sender = st.text_input("Sender (Client Name)")
    recipient = st.text_input("Recipient (Invoice ID)")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if sender and recipient and amount > 0:
            transaction = Transaction(sender, recipient, amount)
            st.session_state.blockchain.add_block([transaction])
            st.success("Transaction added to blockchain!")
        else:
            st.error("Please fill in all fields correctly.")

st.subheader("Blockchain Ledger")

# Display blockchain
for i, block in enumerate(st.session_state.blockchain.chain):
    st.write(f"### Block {i}")
    st.json({
        "Previous Hash": block.previous_hash,
        "Block Hash": block.hash,
        "Transactions": [
            {"Sender": t.sender, "Recipient": t.recipient, "Amount": t.amount}
            for t in block.transactions
        ]
    })

# Validate blockchain
if st.button("🔍 Validate Blockchain Integrity"):
    if st.session_state.blockchain.is_valid():
        st.success("Blockchain is valid ✅")
    else:
        st.error("Blockchain is invalid ❌")
