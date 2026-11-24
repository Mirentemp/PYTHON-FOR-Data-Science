"""
Name: Miren
Date: November 24, 2026
"""

print("=== Patel Stationery Store ===")

notebook_qty = 5
notebook_rate = 62
pen_box_qty = 2
pen_box_rate = 148
file_qty = 1
file_rate = 165

# Calculate and print notebook amount
notebook_amount = notebook_qty * notebook_rate
print("Notebook amount:", notebook_amount)

# Calculate and print pen box amount
pen_box_amount = pen_box_qty * pen_box_rate
print("Pen box amount:", pen_box_amount)

# Calculate and print file amount
file_amount = file_qty * file_rate
print("File amount:", file_amount)

# Part 2: Subtotal, discount, GST, and final bill
subtotal = notebook_amount + pen_box_amount + file_amount
discount_rate = 0.05
discount_amount = subtotal * discount_rate
discounted_amount = subtotal - discount_amount
gst_rate = 0.05
gst_amount = discounted_amount * gst_rate
final_bill = discounted_amount + gst_amount

print("Subtotal:", subtotal)
print("Discount rate:", discount_rate)
print("Discount amount:", discount_amount)
print("GST rate:", gst_rate)
print("Final bill (before rate change):", final_bill)

# Re-assign notebook_rate to 64 and recalculate final_bill
notebook_rate = 64
notebook_amount = notebook_qty * notebook_rate
subtotal = notebook_amount + pen_box_amount + file_amount
discount_amount = subtotal * discount_rate
discounted_amount = subtotal - discount_amount
gst_amount = discounted_amount * gst_rate
final_bill = discounted_amount + gst_amount

print("Final bill (after rate change):", final_bill)

# Demonstrate dynamic typing with bill_status
bill_status = 0
print("Bill status initially:", bill_status)
bill_status = "PAID"
print("Bill status updated:", bill_status)
