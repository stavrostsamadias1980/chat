import { Injectable, signal, OnDestroy } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DeepChatService implements OnDestroy {
  private getWebSocketUrl(): string {
    if (typeof window === 'undefined') return 'ws://localhost:8088/ws/chat';
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    // When running locally in Angular CLI dev server
    if (window.location.port === '4200') {
      return 'ws://localhost:8088/ws/chat';
    }
    // Production (HTTPS -> WSS directly on same host)
    return `${protocol}//${window.location.host}/ws/chat`;
  }

  private socket: WebSocket | null = null;
  private pendingHandlers: any[] = [];
  private reconnectTimer: any = null;

  // Reactive State Signals for UI
  public isConnected = signal<boolean>(false);
  public connectionStatusText = signal<string>('Σύνδεση...');

  constructor() {
    this.connect();
  }

  ngOnDestroy(): void {
    this.disconnect();
  }

  /**
   * Initialize and manage the real-time WebSocket connection to Spring Boot backend
   */
  public connect(): void {
    if (this.socket && (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)) {
      return;
    }

    try {
      const url = this.getWebSocketUrl();
      this.socket = new WebSocket(url);

      this.socket.onopen = () => {
        this.isConnected.set(true);
        this.connectionStatusText.set('Online (WebSocket)');
        console.log('⚡ DeepChatService: WebSocket connected to Spring Boot Backend');
      };

      this.socket.onmessage = (event: MessageEvent) => {
        this.handleIncomingMessage(event);
      };

      this.socket.onclose = () => {
        this.isConnected.set(false);
        this.connectionStatusText.set('Αποσυνδέθηκε (Επανασύνδεση...)');
        this.scheduleReconnect();
      };

      this.socket.onerror = () => {
        this.isConnected.set(false);
        this.connectionStatusText.set('Σφάλμα Σύνδεσης');
      };
    } catch (err) {
      this.isConnected.set(false);
      this.connectionStatusText.set('Offline');
      this.scheduleReconnect();
    }
  }

  public disconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectTimer) return;
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.connect();
    }, 3000);
  }

  /**
   * Generates the Deep Chat connect.handler object
   */
  public getConnectConfig(): { handler: (body: any, signals: any) => void } {
    return {
      handler: (body: any, signals: any) => {
        const messages = body.messages || [];
        const lastMsg = messages.length > 0 ? messages[messages.length - 1] : null;
        const queryText = (lastMsg?.text || body.text || '').trim();

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
          this.connect();
          setTimeout(() => {
            if (this.socket && this.socket.readyState === WebSocket.OPEN) {
              this.pendingHandlers.push(signals);
              this.socket.send(JSON.stringify(payload));
            } else {
              signals.onResponse({ text: '⚠️ Ο server δεν είναι συνδεδεμένος. Παρακαλώ δοκιμάστε ξανά σε λίγο.' });
            }
          }, 1000);
        }
      }
    };
  }

  private handleIncomingMessage(event: MessageEvent): void {
    try {
      const data = JSON.parse(event.data);
      const signalHandler = this.pendingHandlers.shift();
      if (signalHandler) {
        const formattedMarkdown = this.formatRAGResponse(data);
        signalHandler.onResponse({ text: formattedMarkdown });
      }
    } catch (err) {
      console.error('Error handling WebSocket response in DeepChatService:', err);
      const signalHandler = this.pendingHandlers.shift();
      if (signalHandler) {
        signalHandler.onResponse({ text: '⚠️ Σφάλμα επεξεργασίας απάντησης.' });
      }
    }
  }

  /**
   * Formats Spring Boot Extractive RAG Response into rich Markdown
   */
  public formatRAGResponse(data: any): string {
    if (data.status === 'error') {
      return '⚠️ **Σφάλμα:** ' + (data.message || 'Παρουσιάστηκε πρόβλημα κατά την αναζήτηση.');
    }

    const faqs = data.faqs || [];
    const passages = data.passages || [];

    if (faqs.length === 0 && passages.length === 0) {
      return '🔍 **Δεν βρέθηκαν σχετικά αποσπάσματα** στα επίσημα συμβόλαια Anytime για το συγκεκριμένο ερώτημα.\n\n*Δοκιμάστε να ρωτήσετε για καλύψεις αυτοκινήτου, οδική βοήθεια 1158, έκπτωση ΕΝΦΙΑ ή όρους κατοικίας.*';
    }

    let md = '';

    // 1. FAQs
    if (faqs.length > 0) {
      const topFaq = faqs[0];
      md += `### 💡 ${topFaq.question}\n\n`;
      md += `${topFaq.answer}\n\n`;
      if (topFaq.category) {
        md += `*📁 Κατηγορία: **${this.getCategoryName(topFaq.category)}***\n\n`;
      }
    }

    // 2. Passages / Contract Details
    if (passages.length > 0) {
      md += `#### 📋 Αποσπάσματα Όρων Συμβολαίου\n\n`;
      for (const p of passages.slice(0, 2)) {
        const text = p.snippet || p.passage_text;
        md += `> ${text}\n\n`;
        const source = p.contract_name || p.source_file;
        if (source) {
          md += `*📌 Πηγή: **${source}***\n\n`;
        }
      }
    }

    // 3. Emergency Phone 1158
    const qLower = (data.query || '').toLowerCase();
    if (qLower.includes('οδικ') || qLower.includes('τηλεφ') || qLower.includes('βοηθ') || qLower.includes('βλαβ') || qLower.includes('1158')) {
      md += `---\n📞 **Οδική Βοήθεια Anytime:** Καλέστε άμεσα στο **1158** (24/7 εξυπηρέτηση ατυχήματος & βλάβης).\n`;
    }

    return md.trim();
  }

  private getCategoryName(cat: string): string {
    const map: Record<string, string> = {
      car_insurance: 'Αυτοκίνητο',
      home_property_insurance: 'Σπίτι',
      health_insurance: 'Υγεία',
      moto_insurance: 'Μηχανή',
      travel_insurance: 'Ταξίδι',
      cyber_insurance: 'Cyber Risk',
      micro_mobility_ebikes: 'e-Bikes'
    };
    return map[cat] || cat;
  }
}
