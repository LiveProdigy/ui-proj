export interface Meeting {
  id: string;
  title: string;
  description: string;
  meetingDate: string;
  platform: 'teams' | 'zoom' | 'meet';
  thumbnailUrl: string;
  transcript: string;
  notes: string;
  externalLink: string;
  summaries: {
    client: string;
    developer: string;
    coordinator: string;
  };
}

export interface CommunicationFormat {
  id: string;
  name: string;
  channels: string[];
  recipients: string[];
  messageStyle: string;
}

export interface SentCommunication {
  meetingId: string;
  meetingName: string;
  projectName: string;
  formats: {
    channel: string;
    status: 'sent' | 'pending';
  }[];
}

export interface Plugin {
  id: string;
  type: 'teams' | 'outlook' | 'slack';
  profileName: string;
  isActive: boolean;
  lastSynced: string;
}
