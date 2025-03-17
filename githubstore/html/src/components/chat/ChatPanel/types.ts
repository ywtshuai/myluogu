import type { ChatMessage } from '../../../types/chat';

export interface ChatPanelProps {
    messages?: ChatMessage[];
    onSendMessage?: (message: string) => void;
}