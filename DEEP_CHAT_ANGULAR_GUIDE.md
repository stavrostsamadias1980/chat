# 📘 Deep Chat στην Angular — Πλήρης Τεχνικός Οδηγός & Documentation

> **Έκδοση Deep Chat:** 2.5.1+  
> **Έκδοση Angular:** 17 / 18 / 19 / 20+ (Standalone Components & Signals)  
> **Συμβατότητα Backend:** Spring Boot 3 / Pure Java / WebSockets / Node.js / FastAPI / REST  
> **Σκοπός:** Πλήρης τεκμηρίωση εγκατάστασης, αρχιτεκτονικής, theming, κουμπιών, multimedia δυνατοτήτων και real-time WebSocket διασύνδεσης.

---

## 📑 Πίνακας Περιεχομένων

1. [Τι είναι το Deep Chat & Γιατί υπερέχει](#1-τι-είναι-το-deep-chat--γιατί-υπερέχει)
2. [Βήμα 1: Εγκατάσταση στο Angular Project](#2-βήμα-1-εγκατάσταση-στο-angular-project)
3. [Βήμα 2: Αρχιτεκτονική Ενσωμάτωσης στην Angular (Standalone)](#3-βήμα-2-αρχιτεκτονική-ενσωμάτωσης-στην-angular-standalone)
   - [Γιατί απαιτείται το `CUSTOM_ELEMENTS_SCHEMA`](#γιατί-απαιτείται-το-custom_elements_schema)
   - [Δήλωση Imports & Template Binding](#δήλωση-imports--template-binding)
4. [Βήμα 3: Τοποθέτηση στο Layout (Floating Widget Αριστερά / Δεξιά / Embedded)](#4-βήμα-3-τοποθέτηση-στο-layout)
5. [Βήμα 4: Πλήρης Οδηγός Theming & Styling (Χρώματα, Bubbles, Dark Mode)](#5-βήμα-4-πλήρης-οδηγός-theming--styling)
   - [Δομή `chatStyle` (Canvas / Φόντο)](#δομή-chatstyle-canvas--φόντο)
   - [Δομή `messageStyles` (Στρογγυλεμένα Bubbles & Χρώματα)](#δομή-messagestyles-στρογγυλεμένα-bubbles--χρώματα)
   - [Δυναμικό Dark / Light Theme με Angular Signals](#δυναμικό-dark--light-theme-με-angular-signals)
   - [Απευθείας CSS Injection με `auxiliaryStyle` (Shadow DOM bypass)](#απευθείας-css-injection-με-auxiliarystyle)
6. [Βήμα 5: Παραμετροποίηση Buttons & Input Bar](#6-βήμα-5-παραμετροποίηση-buttons--input-bar)
   - [Κουμπί Αποστολής (`submitButtonStyles`)](#κουμπί-αποστολής-submitbuttonstyles)
   - [Μπάρα Εισαγωγής Κειμένου (`textInput`)](#μπάρα-εισαγωγής-κειμένου-textinput)
   - [Custom Action Buttons & Chips](#custom-action-buttons--chips)
7. [Βήμα 6: Multimedia Δυνατότητες πέρα από το AI (Out-of-the-box Features)](#7-βήμα-6-multimedia-δυνατότητες-πέρα-από-το-ai)
   - [🎙️ Speech-to-Text (Φωνητική Είσοδος με Μικρόφωνο)](#-speech-to-text-φωνητική-είσοδος-με-μικρόφωνο)
   - [🔊 Text-to-Speech (Φωνητική Εκφώνηση Απαντήσεων)](#-text-to-speech-φωνητική-εκφώνηση-απαντήσεων)
   - [📎 Αποστολή Αρχείων, Εικόνων & Drag & Drop](#-αποστολή-αρχείων-εικόνων--drag--drop)
   - [📸 Web Camera Snapshot](#-web-camera-snapshot)
   - [💾 Browser Storage & Διατήρηση Ιστορικού (Persistence)](#-browser-storage--διατήρηση-ιστορικού-persistence)
   - [👤 Avatars, Ονόματα & Intro Messages](#-avatars-ονόματα--intro-messages)
8. [Βήμα 7: Διασύνδεση με WebSockets & Custom Backend](#8-βήμα-7-διασύνδεση-με-websockets--custom-backend)
   - [Αρχιτεκτονική Επικοινωνίας (`connect.handler`)](#αρχιτεκτονική-επικοινωνίας-connecthandler)
   - [Ανάλυση Κώδικα Σύνδεσης Βήμα-προς-Βήμα](#ανάλυση-κώδικα-σύνδεσης-βήμα-προς-βήμα)
   - [Μορφοποίηση RAG Extractive Δεδομένων σε Markdown](#μορφοποίηση-rag-extractive-δεδομένων-σε-markdown)
   - [Error Handling & Auto-Reconnect](#error-handling--auto-reconnect)
9. [Ολοκληρωμένος Κώδικας Παραδείγματος (Copy-Paste Ready)](#9-ολοκληρωμένος-κώδικας-παραδείγματος-copy-paste-ready)

---

## 1. Τι είναι το Deep Chat & Γιατί υπερέχει

Το **[Deep Chat](https://deepchat.dev/)** είναι ένα πανίσχυρο, αυτόνομο **Web Component (Custom Element)** φτιαγμένο ειδικά για chat interfaces και AI εφαρμογές.

### Βασικά Πλεονεκτήματα:
1. **Framework Agnostic:** Δεν είναι «μόνο για React» ή «μόνο για Vue». Είναι native HTML custom element (`<deep-chat></deep-chat>`), που σημαίνει ότι λειτουργεί σε **Angular**, React, Vue, Svelte ή ακόμα και σε απλό Vanilla HTML αρχείο.
2. **Zero Dependencies στο UI:** Δεν χρειάζεται Material UI, Bootstrap, Tailwind ή Angular CDK. Όλα τα components, animations, icons και SVG είναι ενσωματωμένα μέσα στο δικό του **Shadow DOM**.
3. **Υποστήριξη WebSockets & Direct Custom Services:** Δεν σας αναγκάζει να χρησιμοποιήσετε OpenAI API. Μπορεί να συνδεθεί με οποιοδήποτε WebSocket ή REST backend έχετε φτιάξει (π.χ. Spring Boot, Python FastAPI, Express).
4. **Out-of-the-Box Multimedia:** Παρέχει έτοιμο Speech-to-Text (μικρόφωνο), Text-to-Speech (φωνητική ανάγνωση), λήψη κάμερας, drag-and-drop αρχείων και markdown formatting χωρίς να γράψετε ούτε μία γραμμή audio/file processing κώδικα!

---

## 2. Βήμα 1: Εγκατάσταση στο Angular Project

Μέσα στο φάκελο της Angular εφαρμογής (π.χ. `UI/`), εκτελείτε στο τερματικό:

```bash
npm install deep-chat --save
```

Το πακέτο εγκαθιστά το Web Component και τα TypeScript type definitions στο `node_modules/deep-chat/`.

---

## 3. Βήμα 2: Αρχιτεκτονική Ενσωμάτωσης στην Angular (Standalone)

### Γιατί απαιτείται το `CUSTOM_ELEMENTS_SCHEMA`

Η Angular από προεπιλογή ελέγχει όλα τα HTML tags στο template σας. Όταν συναντήσει ένα custom HTML tag όπως το `<deep-chat>`, θεωρεί ότι είναι άγνωστο Angular Component και πετάει σφάλμα κατά το compile (`'deep-chat' is not a known element`).

Για να πούμε στην Angular ότι το tag `<deep-chat>` είναι έγκυρο **Web Component**, δηλώνουμε το `CUSTOM_ELEMENTS_SCHEMA`:

```typescript
import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import 'deep-chat'; // Εισάγει και καταχωρεί το custom element στο browser registry

@Component({
  selector: 'app-deep-chat-widget',
  standalone: true,
  imports: [CommonModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA], // <-- ΑΠΑΡΑΙΤΗΤΟ
  templateUrl: './deep-chat-widget.component.html',
  styleUrls: ['./deep-chat-widget.component.scss']
})
export class DeepChatWidgetComponent {
  // logic...
}
```

### Δήλωση Imports & Template Binding

Στο template (`.html`), το χρησιμοποιείτε απλά σαν ένα κανονικό HTML tag με property bindings (`[...]`):

```html
<deep-chat
  [connect]="connectConfig"
  [chatStyle]="chatStyle"
  [messageStyles]="messageStyles"
  [textInput]="textInput"
  [speechToText]="speechToText"
  [introMessage]="introMessage"
  [avatars]="avatars"
  [submitButtonStyles]="submitButtonStyles"
></deep-chat>
```

---

## 4. Βήμα 3: Τοποθέτηση στο Layout

Το Deep Chat μπορεί να τοποθετηθεί με 3 διαφορετικούς τρόπους:

### Τρόπος Α: Floating Widget Αριστερά (Όπως υλοποιήθηκε στο έργο μας)

Στο SCSS του component ορίζουμε `position: fixed` με σημείο αναφοράς την κάτω-αριστερή γωνία:

```scss
/* 1. Floating Στρογγυλό Κουμπί Launcher (Κάτω Αριστερά) */
.deepchat-widget-launcher {
  position: fixed;
  bottom: 20px;
  left: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4f46e5 0%, #0084d6 100%);
  color: #ffffff;
  border: none;
  cursor: pointer;
  z-index: 12001;
  box-shadow: 0 16px 36px rgba(79, 70, 229, 0.35);
  display: grid;
  place-items: center;
}

/* 2. Κυρίως Παράθυρο Chat (Κάτω Αριστερά) */
.deepchat-widget-container {
  position: fixed;
  bottom: 92px;
  left: 16px;
  width: clamp(320px, 94vw, 460px);
  height: clamp(480px, 85vh, 720px);
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 12000;
  
  /* Το deep-chat καταλαμβάνει όλο το διαθέσιμο ύψος */
  deep-chat {
    width: 100%;
    height: 100%;
    display: block;
  }
}
```

### Τρόπος Β: Floating Widget Δεξιά
Αλλάζετε απλά το `left: 20px` σε `right: 20px` και `left: 16px` σε `right: 16px`.

### Τρόπος Γ: Embedded σε Σελίδα / Dashboard (Ενσωματωμένο)
Αν θέλετε το chat να είναι μέρος μιας σελίδας (π.χ. σε μία δεξιά στήλη 400px):

```html
<div class="chat-sidebar" style="width: 400px; height: 600px;">
  <deep-chat style="width: 100%; height: 100%;"></deep-chat>
</div>
```

---

## 5. Βήμα 4: Πλήρης Οδηγός Theming & Styling

Όλο το styling στο Deep Chat ορίζεται με JavaScript objects που περιέχουν CSS properties σε **camelCase** (π.χ. `backgroundColor` αντί για `background-color`).

### Δομή `chatStyle` (Canvas / Φόντο)
Ελέγχει το εξωτερικό container του chat:

```typescript
public chatStyle = {
  width: '100%',
  height: '100%',
  borderRadius: '0px',             // 0 αν είναι ήδη μέσα σε στρογγυλεμένο modal
  border: 'none',
  backgroundColor: '#f8fafc',      // Απαλό background φόντο
  fontFamily: "'Plus Jakarta Sans', sans-serif"
};
```

---

### Δομή `messageStyles` (Στρογγυλεμένα Bubbles & Χρώματα)

Εδώ ρυθμίζεται η εμφάνιση των μηνυμάτων. Χρησιμοποιούμε **ασύμμετρα `borderRadius`** για να ξεχωρίζει ποιος μιλάει:

```typescript
public messageStyles = {
  default: {
    // 🤖 Μηνύματα του Bot (Αριστερά)
    ai: {
      bubble: {
        backgroundColor: '#ffffff',
        color: '#0f172a',
        border: '1px solid #e2e8f0',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
        // Στρογγυλό παντού, αλλά η κάτω-αριστερή γωνία μυτερή (δείχνει προς το bot)
        borderRadius: '18px 18px 18px 4px',
        fontSize: '14px',
        lineHeight: '1.6',
        padding: '12px 16px'
      }
    },
    // 👤 Μηνύματα του Χρήστη (Δεξιά)
    user: {
      bubble: {
        // Gradient χρώμα της Anytime
        background: 'linear-gradient(135deg, #0084d6 0%, #004d80 100%)',
        color: '#ffffff',
        // Στρογγυλό παντού, αλλά η κάτω-δεξιά γωνία μυτερή (δείχνει προς τον χρήστη)
        borderRadius: '18px 18px 4px 18px',
        fontSize: '14px',
        fontWeight: '500',
        padding: '12px 16px'
      }
    }
  },
  // ⏳ Εμφάνιση κατά τη διάρκεια φόρτωσης/σκέψης
  loading: {
    bubble: {
      backgroundColor: '#ffffff',
      border: '1px solid #e2e8f0',
      borderRadius: '16px'
    }
  }
};
```

---

### Δυναμικό Dark / Light Theme με Angular Signals

Μπορείτε να αλλάζετε το theme άμεσα με Angular Signals:

```typescript
import { signal, computed } from '@angular/core';

export class ChatComponent {
  public isDarkMode = signal<boolean>(false);

  // Dynamic Theme Computed Signal
  public currentChatStyle = computed(() => ({
    backgroundColor: this.isDarkMode() ? '#0f172a' : '#ffffff',
    color: this.isDarkMode() ? '#f8fafc' : '#0f172a'
  }));

  public toggleDark(): void {
    this.isDarkMode.update(v => !v);
  }
}
```

---

### Απευθείας CSS Injection με `auxiliaryStyle` (Shadow DOM bypass)

Αν θέλετε να γράψετε **native CSS rules** που θα εφαρμοστούν απευθείας μέσα στο Shadow DOM (π.χ. custom scrollbar, hover transitions, text selection):

```typescript
public customCss = `
  /* Στιλάτη Scrollbar */
  ::-webkit-scrollbar {
    width: 6px;
  }
  ::-webkit-scrollbar-thumb {
    background: #0084d6;
    border-radius: 10px;
  }
  /* Επιλογή κειμένου */
  ::selection {
    background: rgba(0, 132, 214, 0.2);
  }
`;
```

Και στο template:
```html
<deep-chat [auxiliaryStyle]="customCss"></deep-chat>
```

---

## 6. Βήμα 5: Παραμετροποίηση Buttons & Input Bar

### Κουμπί Αποστολής (`submitButtonStyles`)

Μπορείτε να αλλάξετε το χρώμα, το μέγεθος και το εικονίδιο SVG του κουμπιού αποστολής:

```typescript
public submitButtonStyles = {
  submit: {
    container: {
      default: {
        backgroundColor: '#0084d6',
        borderRadius: '10px',
        padding: '6px'
      },
      hover: {
        backgroundColor: '#006eb5'
      }
    },
    svg: {
      styles: {
        default: {
          fill: '#ffffff' // Άσπρο βέλος
        }
      }
    }
  },
  loading: {
    container: {
      default: { backgroundColor: '#cbd5e1' }
    }
  }
};
```

### Μπάρα Εισαγωγής Κειμένου (`textInput`)

Ρυθμίζει το placeholder και τα στυλ του input container:

```typescript
public textInput = {
  placeholder: { 
    text: 'Ρωτήστε για ασφάλεια αυτοκινήτου, σπιτιού ή πατήστε 🎙️...' 
  },
  styles: {
    container: {
      backgroundColor: '#ffffff',
      border: '1.5px solid #e2e8f0',
      borderRadius: '14px',
      boxShadow: '0 2px 6px rgba(0, 0, 0, 0.04)'
    },
    text: {
      fontSize: '14px',
      color: '#0f172a'
    }
  }
};
```

---

## 7. Βήμα 6: Multimedia Δυνατότητες πέρα από το AI

Το Deep Chat ενσωματώνει εντυπωσιακές out-of-the-box δυνατότητες με 1 μόνο configuration property:

### 🎙️ Speech-to-Text (Φωνητική Είσοδος με Μικρόφωνο)
Ενεργοποιεί το native Web Speech API του browser. Εμφανίζει αυτόματα εικονίδιο μικροφώνου δίπλα στο input box:

```typescript
public speechToText = {
  webSpeech: true,
  translations: {
    listen: 'Μιλήστε τώρα (Ακούω)...',
    title: 'Χρήση Μικροφώνου'
  }
};
```

### 🔊 Text-to-Speech (Φωνητική Εκφώνηση Απαντήσεων)
Εκφωνεί φωνητικά τις απαντήσεις που επιστρέφει το σύστημα:

```typescript
public textToSpeech = {
  volume: 0.9,
  rate: 1.0,
  pitch: 1.0
};
```

### 📎 Αποστολή Αρχείων, Εικόνων & Drag & Drop
Υποστηρίζει αποστολή εικόνων και εγγράφων PDF με drag-and-drop:

```typescript
public images = {
  maxNumberOfFiles: 3,
  acceptedFormats: '.png,.jpg,.jpeg,.webp'
};

public mixedFiles = {
  maxNumberOfFiles: 5,
  acceptedFormats: '.pdf,.docx,.txt'
};
```

### 📸 Web Camera Snapshot
Επιτρέπει στο χρήστη να ανοίξει την web κάμερα και να τραβήξει φωτογραφία μέσα από το chat:

```typescript
public camera = true;
```

### 💾 Browser Storage & Διατήρηση Ιστορικού (Persistence)
Αποθηκεύει αυτόματα το ιστορικό της συνομιλίας στο `localStorage` του browser, ώστε αν ο χρήστης κάνει ανανέωση σελίδας (F5) να μη χαθούν τα μηνύματα:

```typescript
public browserStorage = true; // Ή { session: true } για sessionStorage
```

### 👤 Avatars, Ονόματα & Intro Messages

```typescript
public avatars = {
  ai: {
    styles: {
      avatar: { backgroundColor: '#4f46e5', color: '#ffffff' }
    }
  },
  user: {
    styles: {
      avatar: { backgroundColor: '#0084d6', color: '#ffffff' }
    }
  }
};

public introMessage = {
  text: '👋 **Γεια σας!** Είμαι ο ψηφιακός βοηθός της Anytime. Πώς μπορώ να σας εξυπηρετήσω σήμερα;'
};
```

---

## 8. Βήμα 7: Διασύνδεση με WebSockets & Custom Backend

### Αρχιτεκτονική Επικοινωνίας (`connect.handler`)

Ενώ το Deep Chat έχει ένα απλό property `websocket: true`, αυτό περιμένει συγκεκριμένο format μηνυμάτων από το backend.

Στην πραγματική παραγωγή, τα enterprise backends (όπως το δικό μας **Spring Boot 3 Pure Java Backend**) επιστρέφουν εξειδικευμένα payload αντικείμενα (π.χ. `{ status, faqs: [...], passages: [...], total_results }`).

Γι' αυτό, η πιο αξιόπιστη και πανίσχυρη μέθοδος είναι το **`connect.handler`**:

```
[ Χρήστης στο Deep Chat ]
         │
         ▼
[ connect.handler(body, signals) ] ── (Υποκλοπή ερωτήματος & αποστολή)
         │
         ▼
[ WebSocket: ws://localhost:8088/ws/chat ]
         │
         ▼
[ Spring Boot Pure Java Search Engine ]
         │
         ▼ (Επιστροφή FAQs + Passages JSON)
[ WebSocket onmessage ]
         │
         ▼
[ Μετατροπή σε Markdown κείμενο ]
         │
         ▼
[ signals.onResponse({ text: markdown }) ]
         │
         ▼
[ Deep Chat κάνει Render με Markdown, Quotes, Bolds & Links ]
```

---

### Ανάλυση Κώδικα Σύνδεσης Βήμα-προς-Βήμα

Στο component διατηρούμε τη σύνδεση WebSocket και έναν πίνακα αναμονής (`pendingHandlers`):

```typescript
private socket: WebSocket | null = null;
private pendingHandlers: any[] = [];
private readonly wsUrl = 'ws://localhost:8088/ws/chat';

// 1. Άνοιγμα WebSocket
private initWebSocket(): void {
  this.socket = new WebSocket(this.wsUrl);

  this.socket.onopen = () => {
    console.log('⚡ Connected to Spring Boot WebSocket');
  };

  // 2. Λήψη απάντησης από το Backend
  this.socket.onmessage = (event: MessageEvent) => {
    const data = JSON.parse(event.data);
    const handler = this.pendingHandlers.shift();
    if (handler) {
      // Μετατρέπουμε το RAG JSON σε όμορφο Markdown
      const markdown = this.formatRAGResponse(data);
      handler.onResponse({ text: markdown });
    }
  };

  // 3. Αυτόματη επανασύνδεση αν πέσει η σύνδεση
  this.socket.onclose = () => {
    setTimeout(() => this.initWebSocket(), 3000);
  };
}

// 4. Ορισμός του Connect Config για το Deep Chat
public connectConfig = {
  handler: (body: any, signals: any) => {
    const messages = body.messages || [];
    const lastMessage = messages[messages.length - 1];
    const queryText = (lastMessage?.text || '').trim();

    if (!queryText) {
      signals.onResponse({ text: 'Παρακαλώ πληκτρολογήστε ένα ερώτημα.' });
      return;
    }

    const payload = {
      query: queryText,
      category: null,
      top_k: 4
    };

    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.pendingHandlers.push(signals);
      this.socket.send(JSON.stringify(payload));
    } else {
      signals.onResponse({ text: '⚠️ Ο server δεν είναι συνδεδεμένος.' });
    }
  }
};
```

---

### Μορφοποίηση RAG Extractive Δεδομένων σε Markdown

Η μέθοδος αυτή παίρνει τα αυθεντικά συμβόλαια και τα κάνει format σε Markdown, το οποίο το Deep Chat υποστηρίζει εγγενώς:

```typescript
private formatRAGResponse(data: any): string {
  if (data.status === 'error') {
    return '⚠️ **Σφάλμα:** ' + (data.message || 'Πρόβλημα αναζήτησης.');
  }

  const faqs = data.faqs || [];
  const passages = data.passages || [];

  if (faqs.length === 0 && passages.length === 0) {
    return '🔍 **Δεν βρέθηκαν σχετικά αποσπάσματα** στα επίσημα συμβόλαια.';
  }

  let md = '';

  // FAQ Title & Answer
  if (faqs.length > 0) {
    const topFaq = faqs[0];
    md += `### 💡 ${topFaq.question}\n\n`;
    md += `${topFaq.answer}\n\n`;
  }

  // Contract Passages Quotes
  if (passages.length > 0) {
    md += `#### 📋 Αποσπάσματα Όρων Συμβολαίου\n\n`;
    for (const p of passages.slice(0, 2)) {
      md += `> ${p.snippet || p.passage_text}\n\n`;
      if (p.contract_name) {
        md += `*📌 Πηγή: **${p.contract_name}***\n\n`;
      }
    }
  }

  // Έλεγχος για Οδική Βοήθεια 1158
  const q = (data.query || '').toLowerCase();
  if (q.includes('οδικ') || q.includes('βοηθ') || q.includes('1158')) {
    md += `---\n📞 **Οδική Βοήθεια Anytime:** Καλέστε στο **1158** (24/7 εξυπηρέτηση).\n`;
  }

  return md.trim();
}
```

---

## 9. Ολοκληρωμένος Κώδικας Παραδείγματος (Copy-Paste Ready)

### TypeScript: `my-chat.component.ts`

```typescript
import { Component, OnInit, OnDestroy, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import 'deep-chat';

@Component({
  selector: 'app-my-chat',
  standalone: true,
  imports: [CommonModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  template: `
    <div class="chat-wrapper">
      <deep-chat
        [connect]="connectConfig"
        [chatStyle]="chatStyle"
        [messageStyles]="messageStyles"
        [textInput]="textInput"
        [speechToText]="speechToText"
        [introMessage]="introMessage"
        [avatars]="true"
      ></deep-chat>
    </div>
  `,
  styles: [`
    .chat-wrapper {
      width: 420px;
      height: 650px;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 15px 40px rgba(0,0,0,0.12);
    }
    deep-chat {
      width: 100%;
      height: 100%;
    }
  `]
})
export class MyChatComponent implements OnInit, OnDestroy {
  private socket!: WebSocket;
  private pendingSignals: any[] = [];

  public chatStyle = {
    backgroundColor: '#f8fafc',
    fontFamily: "'Plus Jakarta Sans', sans-serif"
  };

  public messageStyles = {
    default: {
      ai: {
        bubble: {
          backgroundColor: '#ffffff',
          color: '#0f172a',
          borderRadius: '18px 18px 18px 4px',
          border: '1px solid #e2e8f0',
          padding: '12px 16px'
        }
      },
      user: {
        bubble: {
          background: 'linear-gradient(135deg, #0084d6 0%, #004d80 100%)',
          color: '#ffffff',
          borderRadius: '18px 18px 4px 18px',
          padding: '12px 16px'
        }
      }
    }
  };

  public textInput = {
    placeholder: { text: 'Ρωτήστε κάτι ή μιλήστε στο 🎙️...' }
  };

  public speechToText = {
    webSpeech: true
  };

  public introMessage = {
    text: '👋 **Καλώς ήρθατε!** Πώς μπορώ να σας εξυπηρετήσω;'
  };

  public connectConfig = {
    handler: (body: any, signals: any) => {
      const messages = body.messages || [];
      const query = messages[messages.length - 1]?.text || '';
      
      this.pendingSignals.push(signals);
      this.socket.send(JSON.stringify({ query }));
    }
  };

  ngOnInit(): void {
    this.socket = new WebSocket('ws://localhost:8088/ws/chat');
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const signal = this.pendingSignals.shift();
      if (signal) {
        signal.onResponse({ text: data.answer || 'Απάντηση ελήφθη.' });
      }
    };
  }

  ngOnDestroy(): void {
    this.socket?.close();
  }
}
```

---

## 🏁 Συμπέρασμα

Με τον παραπάνω οδηγό, το **Deep Chat**:
1. Ενσωματώνεται άψογα στην **Angular** χωρίς conflict με το zone/change detection μέσω `CUSTOM_ELEMENTS_SCHEMA`.
2. Μπορεί να τοποθετηθεί οπουδήποτε (αριστερά, δεξιά, floating modal, ή embedded dashboard).
3. Υποστηρίζει πλήρες **Theming** με στρογγυλεμένα bubbles, custom gradients, dark mode και direct CSS injection.
4. Προσφέρει **Speech-to-Text**, αρχεία και κάμερα χωρίς επιπλέον βιβλιοθήκες.
5. Συνδέεται αξιόπιστα με **WebSockets** μέσω του `connect.handler`, κάνοντας parse και format σε Markdown οποιαδήποτε δεδομένα επιστρέφει το Backend!
