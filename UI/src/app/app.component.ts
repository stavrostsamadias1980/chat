import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DeepChatWidgetComponent } from './components/deep-chat-widget/deep-chat-widget.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, DeepChatWidgetComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Anytime.gr AI Assistant';
}
