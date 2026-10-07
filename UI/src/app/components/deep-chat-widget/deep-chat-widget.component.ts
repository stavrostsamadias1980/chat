import { Component, OnInit, signal, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DeepChatService } from '../../services/deep-chat.service';
import 'deep-chat';

@Component({
  selector: 'app-deep-chat-widget',
  standalone: true,
  imports: [CommonModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  templateUrl: './deep-chat-widget.component.html',
  styleUrls: ['./deep-chat-widget.component.scss']
})
export class DeepChatWidgetComponent implements OnInit {
  public isOpen = signal<boolean>(true);

  // Deep Chat Configuration Objects (Pure UI Presentation)
  public connectConfig: any;
  public chatStyle: any;
  public messageStyles: any;
  public textInput: any;
  public speechToText: any;
  public introMessage: any;
  public avatars: any;
  public submitButtonStyles: any;

  constructor(public chatService: DeepChatService) {}

  ngOnInit(): void {
    // Delegate WebSocket connection handling to DeepChatService
    this.connectConfig = this.chatService.getConnectConfig();

    // Initialize UI Themes & Presentation Configurations
    this.initUIConfig();
  }

  public toggleWidget(): void {
    this.isOpen.update(val => !val);
  }

  private initUIConfig(): void {
    // 1. UI Layout Styling
    this.chatStyle = {
      width: '100%',
      height: '100%',
      borderRadius: '0px',
      border: 'none',
      backgroundColor: '#f8fafc',
      fontFamily: "'Plus Jakarta Sans', sans-serif"
    };

    // 2. Message Bubbles Styling (Asymmetric Rounded Corners)
    this.messageStyles = {
      default: {
        ai: {
          bubble: {
            backgroundColor: '#ffffff',
            color: '#0f172a',
            border: '1px solid #e2e8f0',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
            borderRadius: '18px 18px 18px 4px',
            fontSize: '14px',
            lineHeight: '1.6'
          }
        },
        user: {
          bubble: {
            background: 'linear-gradient(135deg, #0084d6 0%, #004d80 100%)',
            color: '#ffffff',
            borderRadius: '18px 18px 4px 18px',
            fontSize: '14px',
            fontWeight: '500'
          }
        }
      }
    };

    // 3. Speech to Text (Web Speech API)
    this.speechToText = {
      webSpeech: true,
      translations: {
        listen: 'Μιλήστε τώρα...',
        title: 'Χρήση Μικροφώνου'
      }
    };

    // 4. Input Area Styling
    this.textInput = {
      placeholder: { text: 'Ρωτήστε το Deep Chat ή μιλήστε στο μικρόφωνο 🎙️...' },
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

    // 5. Submit Button Style
    this.submitButtonStyles = {
      submit: {
        svg: {
          styles: {
            default: {
              filter: 'brightness(0) saturate(100%) invert(27%) sepia(91%) saturate(2321%) hue-rotate(224deg) brightness(97%) contrast(92%)'
            }
          }
        }
      }
    };

    // 6. Avatars
    this.avatars = {
      ai: {
        styles: {
          avatar: {
            backgroundColor: '#0084d6',
            color: '#ffffff'
          }
        }
      },
      user: {
        styles: {
          avatar: {
            backgroundColor: '#4f46e5',
            color: '#ffffff'
          }
        }
      }
    };

    // 7. Intro Message
    this.introMessage = {
      text: '🤖 **Καλώς ήρθατε στο Deep Chat AI!**\n\nΕίμαι το επίσημο **Deep Chat Web Component** ενσωματωμένο στην Angular και συνδεδεμένο σε πραγματικό χρόνο με το **Anytime RAG Backend**.\n\n✨ **Δυνατότητες:**\n- 🎙️ **Φωνητική είσοδος** (πατήστε το μικρόφωνο κάτω δεξιά)\n- ⚡ **Real-Time WebSockets** (sub-100ms)\n- 📄 **Extractive RAG** με επίσημα συμβόλαια Anytime\n\n*Δοκιμάστε να ρωτήσετε: «Ποιες καλύψεις έχει το Standard Drive;» ή «Ποιο είναι το τηλέφωνο για οδική βοήθεια;»*'
    };
  }
}
