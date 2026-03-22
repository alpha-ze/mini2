# 🧪 Test Prompts for Each Category

Use these sample grievances to test the AI classification system.

---

## 1. IT / Network

### High Confidence (Should classify correctly)
```
The wifi is not working in my hostel room 301
```
```
I cannot access the college portal to download my exam results
```
```
My laptop cannot connect to the campus network
```
```
The printer in computer lab is not working
```
```
College website is showing error when I try to login
```
```
Internet connection is very slow in the library
```
```
Cannot access email on college server
```
```
Projector in classroom 205 is not turning on
```

### Medium Confidence
```
Need help with online course registration system
```
```
Software installation issue in lab computers
```

---

## 2. Hostel

### High Confidence
```
The food quality in mess is very poor today
```
```
Water is not coming in my hostel bathroom
```
```
AC in room 402 is not cooling properly
```
```
Hostel warden is not responding to complaints
```
```
My roommate is creating disturbance at night
```
```
Mess food tastes bad and unhygienic
```
```
Bed mattress is torn and needs replacement
```
```
Laundry service is not available this week
```
```
Hostel room door lock is broken
```

### Medium Confidence
```
Need permission for late night entry
```
```
Hostel electricity bill is too high
```

---

## 3. Infrastructure

### High Confidence
```
Ceiling fan in classroom 301 is not working
```
```
AC in auditorium is making loud noise
```
```
Broken chair in lecture hall needs repair
```
```
Classroom door is damaged and won't close
```
```
Light bulbs are not working in corridor
```
```
Water leaking from ceiling in building A
```
```
Cracks on the wall of classroom 205
```
```
Broken window glass in lab
```
```
Floor tiles are broken in the entrance
```

### Medium Confidence
```
Need more benches in the cafeteria
```
```
Parking area needs better lighting
```

---

## 4. Academic

### High Confidence
```
Professor is not coming to class regularly
```
```
Need clarification on assignment deadline
```
```
Course syllabus is not uploaded on portal
```
```
Teacher is not responding to emails
```
```
Lecture notes are not provided for last week
```
```
Class timing conflicts with another subject
```
```
Need extra classes for difficult topics
```
```
Project guidelines are not clear
```

### Medium Confidence
```
Want to change my elective subject
```
```
Need study materials for upcoming exam
```

---

## 5. Examination

### High Confidence
```
My exam marks are not updated on portal
```
```
Answer sheet evaluation seems incorrect
```
```
Exam hall ticket is not generated
```
```
Wrong marks entered for my test
```
```
Need revaluation for my exam paper
```
```
Exam schedule has timing conflicts
```
```
Hall ticket download link is not working
```
```
Exam result is not declared yet
```

### Medium Confidence
```
Need admit card for upcoming exam
```
```
Question paper had printing errors
```

---

## 6. Library

### High Confidence
```
Book I requested is not available in library
```
```
Library fine is charged incorrectly
```
```
Cannot find reference books for my subject
```
```
Library card is not working at entry gate
```
```
Need to extend book return deadline
```
```
Digital library access is not working
```
```
Librarian is not issuing books properly
```
```
Reading room is too noisy
```

### Medium Confidence
```
Need more copies of popular textbooks
```
```
Library timing should be extended
```

---

## 7. Administration

### High Confidence
```
Need bonafide certificate for bank account
```
```
ID card is damaged and needs replacement
```
```
Fee receipt is not generated after payment
```
```
Scholarship amount is not credited
```
```
Need NOC for internship application
```
```
Document verification is taking too long
```
```
Fee refund is pending for 2 months
```
```
Admission office is not responding
```
```
Certificate collection process is unclear
```

### Medium Confidence
```
Need transfer certificate urgently
```
```
Payment gateway is not working for fees
```

---

## 8. Discipline / Harassment

### High Confidence
```
Senior students are ragging freshers in hostel
```
```
Facing harassment from classmate
```
```
Bullying incident in campus
```
```
Inappropriate behavior by staff member
```
```
Safety concern in campus at night
```
```
Verbal abuse by senior students
```
```
Discrimination based on background
```

### Medium Confidence
```
Security guard is not allowing entry
```
```
Feeling unsafe in certain areas
```

---

## 9. Other

### Examples (Unclear category)
```
General complaint about campus cleanliness
```
```
Suggestion for improving facilities
```
```
Feedback about college events
```
```
Query about campus rules
```

---

## Testing Instructions

### Test Flow:
1. Send "start" to WhatsApp bot
2. Choose "1" for anonymous
3. Copy-paste one of the prompts above
4. Check if AI classifies correctly
5. Note the confidence score

### Expected Results:

**High Confidence Prompts:**
- Should classify correctly (75-95% confidence)
- Should auto-select category
- Should show "Detected Category: [Correct Category]"

**Medium Confidence Prompts:**
- May classify correctly (60-75% confidence)
- Might ask for manual selection
- Good for testing edge cases

### Evaluation Criteria:

✅ **Good Classification:**
- Confidence > 75%
- Correct category
- Fast response

⚠️ **Needs Improvement:**
- Confidence 60-75%
- Correct but low confidence
- Consider adding more keywords

❌ **Poor Classification:**
- Confidence < 60%
- Wrong category
- Needs keyword updates

---

## Advanced Testing

### Multi-keyword Prompts (Should have high confidence):
```
The wifi internet connection is not working in my hostel room and I cannot access the college portal
```
Expected: IT / Network (90%+)

```
Hostel mess food quality is bad and the dining area is not clean
```
Expected: Hostel (85%+)

```
Classroom AC is broken and the fan is also not working
```
Expected: Infrastructure (85%+)

### Ambiguous Prompts (May need manual selection):
```
Teacher is not available in office
```
Could be: Academic or Administration

```
Cannot submit assignment online
```
Could be: Academic or IT / Network

```
Room is too hot
```
Could be: Hostel or Infrastructure

---

## Testing Checklist

- [ ] Test all 9 categories
- [ ] Test high confidence prompts
- [ ] Test medium confidence prompts
- [ ] Test ambiguous prompts
- [ ] Test multi-keyword prompts
- [ ] Verify confidence scores
- [ ] Check category accuracy
- [ ] Test manual override
- [ ] Test duplicate detection
- [ ] Test SLA prediction

---

## Results Template

Use this to track your testing:

| Prompt | Expected | Actual | Confidence | Status |
|--------|----------|--------|------------|--------|
| "Wifi not working" | IT / Network | IT / Network | 75% | ✅ |
| "Food is bad" | Hostel | Hostel | 85% | ✅ |
| ... | ... | ... | ... | ... |

---

## Tips for Better Classification

### For Users:
1. **Be specific:** "Wifi not working in room 301" > "Internet issue"
2. **Include keywords:** Mention specific items (wifi, food, exam, etc.)
3. **Add location:** Room numbers, building names help context
4. **One issue per grievance:** Don't mix multiple problems

### For Improving AI:
1. **Add keywords:** Update classifier.py with more terms
2. **Adjust weights:** Increase confidence for certain matches
3. **Train custom model:** Use real data to fine-tune DistilBERT
4. **Monitor accuracy:** Track misclassifications and improve

---

## Quick Test Commands

### Test IT / Network:
```
start
1
The wifi is not working in my hostel room
```

### Test Hostel:
```
start
1
The mess food quality is very poor
```

### Test Infrastructure:
```
start
1
AC in classroom 301 is not working
```

### Test Academic:
```
start
1
Professor is not coming to class regularly
```

### Test Examination:
```
start
1
My exam marks are not updated on portal
```

### Test Library:
```
start
1
Book I requested is not available in library
```

### Test Administration:
```
start
1
Need bonafide certificate for bank account
```

### Test Tracking:
```
track GRV-000001
```

---

**Happy Testing! 🧪**

Monitor the bot logs to see classification results in real-time:
```
✅ Classification result: {"department":"IT / Network","confidence":0.75,...}
```
