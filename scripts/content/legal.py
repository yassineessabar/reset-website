"""Legal page content (Australia). Drafts: bracketed items are placeholders, and every page must be
reviewed by a lawyer before launch. Rendered by scripts/build_pages.py into privacy.html, terms.html, accessibility.html."""
UPDATED = '18 October 2026'
ENTITY = '[RESET Pty Ltd, ABN 00 000 000 000]'
CONTACT = 'hello@resetcleaning.app'
PRIVACY_CONTACT = 'privacy@resetcleaning.app'

PAGES = {
'privacy': {
  'title': 'Privacy Policy',
  'summary': 'What personal information we collect, how we use it and your choices.',
  'meta': 'How RESET collects, uses and protects your personal information, in line with the Australian Privacy Principles.',
  'intro': f'This policy explains how {ENTITY} ("RESET", "we") handles your personal information when you use our website, apps and services. We follow the Privacy Act 1988 (Cth) and the Australian Privacy Principles.',
  'sections': [
    ('Information we collect', [
      'We collect what we need to book, deliver and improve your resets:',
      ('ul', ['Contact details: your name, email, mobile number and address.',
              'Home and access details: home size, access instructions, key or door code arrangements, and any notes you leave for your RESET member.',
              'Booking details: dates, services, rhythm, ratings, tips and messages.',
              'Payment details, processed by our payment provider. We do not store full card numbers.',
              'Device and usage information, such as pages visited and app activity, collected with cookies and similar tools.',
              'If you apply to clean with RESET: your work eligibility, experience, availability, and the results of identity and background checks you agree to.']),
    ]),
    ('How we use it', [
      ('ul', ['To book, schedule and deliver your visits, and to tell you when we arrive and leave.',
              'To match you with a RESET member and share what they need to do the job.',
              'To take payments, issue invoices and handle gift cards.',
              'To keep people and homes safe, including identity and background checks for RESET members.',
              'To answer questions, resolve problems and improve our services.',
              'To send you news and offers, if you agree. You can opt out at any time.']),
    ]),
    ('Who we share it with', [
      'We share personal information only when we need to:',
      ('ul', ['The RESET member assigned to your visit, who sees your first name, address, access details and visit notes.',
              'Service providers who help us run RESET, such as payment, messaging, hosting and background-check providers, under contracts that protect your information.',
              'Authorities, when the law requires it or to protect someone\'s safety.']),
      'Some of our providers may store information outside Australia. Where that happens, we take reasonable steps to make sure it is protected in line with the Australian Privacy Principles. [List countries before launch.]',
    ]),
    ('Keeping it safe', [
      'We protect personal information with access controls, encryption in transit and staff training. Access details for your home are visible only to the RESET member on your visit and the people who support it. We keep information only as long as we need it, then delete or de-identify it.',
    ]),
    ('Cookies', [
      'We use cookies to keep you signed in, remember your preferences and understand how our website is used. You can control cookies in your browser settings.',
    ]),
    ('Access, correction and complaints', [
      f'You can ask to see or correct the personal information we hold about you by emailing {PRIVACY_CONTACT}. If you have a privacy complaint, contact us first and we will respond within 30 days. If you are not satisfied, you can contact the Office of the Australian Information Commissioner at oaic.gov.au.',
    ]),
    ('Contact us', [f'{ENTITY}, [street address, Sydney NSW]. Email {PRIVACY_CONTACT}.']),
  ]},

'terms': {
  'title': 'Terms of Service',
  'summary': 'The terms for booking and using RESET.',
  'meta': 'The terms for booking and using RESET home cleaning, gift cards and our website and apps.',
  'intro': f'These terms apply when you book or use RESET, offered by {ENTITY}. By booking, you agree to them. Nothing in these terms limits your rights under the Australian Consumer Law.',
  'sections': [
    ('Booking a reset', [
      'You can book through our website or the RESET app. A booking is confirmed when we tell you it is confirmed in the app or by email. We will match you with a background-checked RESET member and tell you who is coming before they arrive.',
    ]),
    ('Prices and payment', [
      'You see your price before you confirm a booking. We charge the payment method on your account after the visit, unless we tell you otherwise. Prices include GST. [Confirm payment timing before launch.]',
    ]),
    ('Access and keys', [
      'You are responsible for giving safe access to your home at the booked time, by being home, leaving a key or sharing a door code. We keep keys and codes secure and return keys when the visit is done.',
    ]),
    ('Changes and cancellations', [
      'You can change, pause or cancel visits in the app. Our Cancellation & Refund Policy explains the free change window and when a late cancellation fee applies.',
    ]),
    ('If something isn\'t right', [
      'Tell us after your visit and we will make it right, usually by coming back. Our services come with guarantees that cannot be excluded under the Australian Consumer Law, including that they will be provided with due care and skill.',
    ]),
    ('Your home', [
      ('ul', ['Let us know about pets, fragile items and anything that needs special care.',
              'Put away valuables, cash and important documents.',
              'Make sure your home is safe to work in, with water and power available.']),
    ]),
    ('Gift cards', [
      'RESET gift cards can be used towards any reset until the balance runs out, and are valid for at least three years from purchase. Our Gift Card Terms have the details.',
    ]),
    ('Accounts', [
      'Keep your login details private and tell us straight away if you think someone else has used your account. You must be 18 or over to book.',
    ]),
    ('Liability', [
      'To the extent the law allows, our liability for loss or damage is limited to supplying the service again or paying the cost of having it supplied again. This does not affect your rights under the Australian Consumer Law. [Confirm insurance cover and wording before launch.]',
    ]),
    ('Changes to these terms', [
      'We may update these terms from time to time. If a change matters, we will tell you before it applies to your bookings.',
    ]),
    ('Governing law', ['These terms are governed by the laws of New South Wales, Australia.']),
    ('Contact us', [f'{ENTITY}, [street address, Sydney NSW]. Email {CONTACT}.']),
  ]},

'accessibility': {
  'title': 'Accessibility',
  'summary': 'How we make RESET usable for everyone, and how to tell us when it is not.',
  'meta': 'How RESET makes its website and apps usable for everyone, and how to tell us when something gets in the way.',
  'intro': 'Everyone should be able to book a reset or apply to clean, whatever device or assistive technology they use. We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.2 at level AA.',
  'sections': [
    ('What we do', [
      ('ul', ['Every page can be used with a keyboard, with a visible focus indicator.',
              'Text and controls meet colour contrast requirements in our black and white design.',
              'Images that carry information have text alternatives; decorative images are hidden from screen readers.',
              'Form fields have visible labels, and errors say what went wrong and how to fix it.',
              'Animations are reduced when your device asks for reduced motion.',
              'Our name is shown in the RESET logo lettering and is read aloud as "RESET".']),
    ]),
    ('Known limitations', [
      'The map on our booking page is provided by OpenStreetMap and may not be fully accessible to screen readers. You can book without it: the address field is all you need. [Review remaining issues before launch.]',
    ]),
    ('Tell us what gets in the way', [
      f'If something on our website or apps is hard to use, email {CONTACT} with the page and what happened. We will reply within five business days and can help you book another way.',
    ]),
  ]},

'cookies': {
  'title': 'Cookie Policy',
  'summary': 'The cookies and similar tools we use, and how to control them.',
  'meta': 'How RESET uses cookies and similar technologies on its website and apps, and how you can control them.',
  'intro': 'Cookies are small files stored on your device. We use them, and similar tools in our apps, to keep RESET working, remember your choices and understand how people use our website.',
  'sections': [
    ('Cookies we use', [
      ('ul', ['Essential: keep you signed in, protect forms and remember what you entered while booking. These are always on.',
              'Preferences: remember your city and language.',
              'Analytics: help us understand which pages are used and where people get stuck, so we can improve them. [Name the analytics provider before launch.]',
              'Marketing: only if you agree, to measure our advertising. [Remove this item if no marketing cookies are used.]']),
    ]),
    ('Your choices', [
      'You can accept or decline non-essential cookies when you first visit, and change your mind at any time from the cookie settings link in our footer. You can also block or delete cookies in your browser settings, although some parts of RESET may then stop working.',
    ]),
    ('More information', ['To learn how we handle personal information more broadly, read our Privacy Policy. Questions: ' + PRIVACY_CONTACT + '.']),
  ]},

'refunds': {
  'title': 'Cancellation & Refund Policy',
  'summary': 'Changing or cancelling a visit, and what happens if something isn\'t right.',
  'meta': 'How to change or cancel a RESET visit, late cancellation, and refunds when something isn\'t right.',
  'intro': 'Plans change. This policy explains how to change or cancel a visit, and what we do if a reset is not up to standard. It sits alongside our Terms of Service and does not limit your rights under the Australian Consumer Law.',
  'sections': [
    ('Changing or cancelling a visit', [
      'You can change, pause or cancel any visit in the RESET app or on our website.',
      ('ul', ['More than [24 hours] before the visit: free.',
              'Less than [24 hours] before the visit: a late cancellation fee of [amount] may apply, because your RESET member has set that time aside for you.',
              'If we cannot get in at the booked time (no key, no code, nobody home): the visit may be charged as a late cancellation. [Confirm all amounts and windows before launch.]']),
    ]),
    ('If we need to change a visit', [
      'If your RESET member is unwell or something else gets in the way, we will tell you as early as we can and offer another time. If none suits you, you will not be charged.',
    ]),
    ('If something isn\'t right', [
      'Tell us within [48 hours] of your visit, ideally with photos. We will come back and put it right at no cost. If we cannot fix it, or the problem is major, you can choose a refund for the affected part of the visit.',
      'Under the Australian Consumer Law, services must be provided with due care and skill. If a service fails to meet a consumer guarantee, you are entitled to a remedy, which may include a refund.',
    ]),
    ('How refunds are paid', ['Refunds go back to the original payment method, usually within [5 to 10] business days. Gift card payments are refunded to the gift card balance.']),
    ('Contact us', ['Email ' + CONTACT + ' or use Help in the RESET app.']),
  ]},

'gift-card-terms': {
  'title': 'Gift Card Terms',
  'summary': 'How RESET gift cards work, when they expire and how to use them.',
  'meta': 'Terms for buying and using RESET gift cards in Australia, including expiry and balances.',
  'intro': 'These terms apply to RESET gift cards bought on our website or in our apps. They form part of our Terms of Service.',
  'sections': [
    ('Using a gift card', [
      ('ul', ['A gift card can be used towards any RESET visit booked in Australia.',
              'Add it to your RESET account with its code. The balance is used before your other payment method.',
              'Any unused balance stays on the card until it is used or expires.']),
    ]),
    ('Expiry', ['RESET gift cards are valid for at least three years from the date of purchase, as required by Australian law. The expiry date is shown on the gift card and in the email it comes with.']),
    ('Refunds and cash', ['Gift cards cannot be exchanged for cash or refunded, except where the law requires it. If a visit paid with a gift card is refunded, the amount returns to the gift card balance.']),
    ('Lost or stolen cards', ['Treat a gift card code like cash. If you think a code has been used by someone else, contact us straight away and we will help where we can.']),
    ('Fees', ['There are no fees to buy, activate or use a RESET gift card.']),
    ('Contact us', ['Email ' + CONTACT + '.']),
  ]},

'member-terms': {
  'title': 'RESET Member Terms',
  'summary': 'The terms for people who clean with RESET.',
  'meta': 'Terms for RESET members: how visits, checks, payments, safety and conduct work when you clean with RESET.',
  'intro': 'These terms apply to people who clean homes through RESET ("RESET members"). [Decide with a lawyer whether RESET members are engaged as employees or independent contractors, and update these terms to match, including award and superannuation obligations, before launch.]',
  'sections': [
    ('Joining RESET', [
      ('ul', ['You must have the right to work in Australia and be 18 or over.',
              'You agree to an identity check and a background check before your first visit, and to repeat checks from time to time.',
              '[If engaged as contractors: you must hold an active ABN.]']),
    ]),
    ('Choosing visits', ['You choose when you are available in the RESET Team app and which visits you accept. Once you accept a visit, please arrive within the agreed window or tell us as early as you can if you cannot.']),
    ('Doing the visit', [
      ('ul', ['Follow the visit checklist and the customer\'s notes.',
              'Use the kit RESET provides and follow its safety instructions.',
              'Treat every home, key and access code with care. Keys and codes are used only for the visit and returned or forgotten as soon as it is done.',
              'Leave the note: “All done. You can breathe.”']),
    ]),
    ('Payment', ['You are paid for every completed visit, plus any tips, to your nominated bank account. [Set pay rates, timing and how tips are passed on before launch.]']),
    ('Safety', ['Never put yourself at risk. If a home is unsafe, leave and contact us. Report any injury, damage or incident in the app straight away. [Confirm insurance cover before launch.]']),
    ('Conduct and privacy', ['Respect customers\' privacy: do not share photos, information or details about any home. Customer information is used only to complete the visit.']),
    ('Ending the arrangement', ['You can stop cleaning with RESET at any time. We may stop offering you visits for serious or repeated breaches of these terms, after giving you a chance to respond where appropriate.']),
    ('Contact us', ['Email team@resetcleaning.app or use Help in the RESET Team app.']),
  ]},

'complaints': {
  'title': 'Complaints',
  'summary': 'How to raise a complaint and what happens next.',
  'meta': 'How to make a complaint to RESET, how we handle it, and where to go if you are not satisfied.',
  'intro': 'If something has gone wrong, we want to know. This is how to raise a complaint and what you can expect from us.',
  'sections': [
    ('How to complain', [
      ('ul', ['In the RESET app: open the visit and choose Help.',
              'By email: ' + CONTACT + '.',
              'Tell us what happened, when, and what you would like us to do. Photos help.']),
    ]),
    ('What happens next', [
      ('ul', ['We acknowledge your complaint within [1 business day].',
              'We aim to resolve it within [10 business days], and keep you updated if it takes longer.',
              'We tell you the outcome and the reasons for it.']),
    ]),
    ('If you are not satisfied', [
      'You can ask for your complaint to be reviewed by a senior member of our team. If it is still not resolved, you can contact NSW Fair Trading at fairtrading.nsw.gov.au. For privacy complaints, you can contact the Office of the Australian Information Commissioner at oaic.gov.au.',
    ]),
  ]},
}
