import { Meeting, CommunicationFormat, SentCommunication, Plugin } from '../types';

export const mockMeetings: Meeting[] = [
  {
    id: '1',
    title: 'Q1 Product Planning',
    description: 'Quarterly planning session for product roadmap and feature prioritization',
    meetingDate: '2025-10-03T14:00:00Z',
    platform: 'teams',
    thumbnailUrl: 'https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=400',
    transcript: 'Full transcript of the meeting...',
    notes: 'Key decisions made during the meeting...',
    externalLink: 'https://read.ai/meetings/q1-planning',
    summaries: {
      client: 'We discussed the upcoming product features and timeline for Q1 delivery.',
      developer: 'Technical requirements: API integration, database schema updates, new UI components.',
      coordinator: 'Action items assigned to team members with deadlines for next sprint.'
    }
  },
  {
    id: '2',
    title: 'Design System Review',
    description: 'Review of the new design system components and guidelines',
    meetingDate: '2025-10-02T10:30:00Z',
    platform: 'zoom',
    thumbnailUrl: 'https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&cs=tinysrgb&w=400',
    transcript: 'Design system discussion transcript...',
    notes: 'Approved new color palette and typography scale...',
    externalLink: 'https://read.ai/meetings/design-review',
    summaries: {
      client: 'New design direction approved with modern aesthetic and improved accessibility.',
      developer: 'Component library to be updated with new styles. Migration guide needed.',
      coordinator: 'Design team to deliver assets by end of week. Development starts Monday.'
    }
  },
  {
    id: '3',
    title: 'Sprint Retrospective',
    description: 'Team retrospective for Sprint 12',
    meetingDate: '2025-10-01T16:00:00Z',
    platform: 'meet',
    thumbnailUrl: 'https://images.pexels.com/photos/3183197/pexels-photo-3183197.jpeg?auto=compress&cs=tinysrgb&w=400',
    transcript: 'Retrospective discussion...',
    notes: 'Team identified blockers and improvement areas...',
    externalLink: 'https://read.ai/meetings/retro-12',
    summaries: {
      client: 'Sprint completed successfully with all major deliverables met on schedule.',
      developer: 'Identified technical debt items and performance optimization opportunities.',
      coordinator: 'Process improvements identified: better estimation, daily standups adjusted.'
    }
  },
  {
    id: '4',
    title: 'Client Onboarding',
    description: 'Initial meeting with new client to discuss project requirements',
    meetingDate: '2025-09-30T13:00:00Z',
    platform: 'teams',
    thumbnailUrl: 'https://images.pexels.com/photos/3184338/pexels-photo-3184338.jpeg?auto=compress&cs=tinysrgb&w=400',
    transcript: 'Client onboarding transcript...',
    notes: 'Client requirements and expectations documented...',
    externalLink: 'https://read.ai/meetings/onboarding',
    summaries: {
      client: 'Welcome aboard! Looking forward to delivering exceptional results for your project.',
      developer: 'Tech stack confirmed: React, Node.js, PostgreSQL. Timeline: 12 weeks.',
      coordinator: 'Contracts signed. Kickoff scheduled for next week. Resources allocated.'
    }
  }
];

export const mockFormats: CommunicationFormat[] = [
  {
    id: '1',
    name: 'Stakeholder Updates',
    channels: ['outlook', 'teams'],
    recipients: ['client@example.com', 'manager@example.com'],
    messageStyle: 'Professional and concise summary focusing on business outcomes'
  },
  {
    id: '2',
    name: 'Developer Briefings',
    channels: ['slack'],
    recipients: ['dev-team'],
    messageStyle: 'Technical details with code snippets and architecture notes'
  }
];

export const mockSentCommunications: SentCommunication[] = [
  {
    meetingId: '1',
    meetingName: 'Q1 Product Planning',
    projectName: 'Project Alpha',
    formats: [
      { channel: 'Teams Chat', status: 'sent' },
      { channel: 'Slack', status: 'sent' },
      { channel: 'Mail to Stakeholders', status: 'pending' },
      { channel: 'Mail to Developers', status: 'sent' }
    ]
  },
  {
    meetingId: '2',
    meetingName: 'Design System Review',
    projectName: 'Design System v2',
    formats: [
      { channel: 'Teams Chat', status: 'sent' },
      { channel: 'Mail to Stakeholders', status: 'sent' }
    ]
  },
  {
    meetingId: '3',
    meetingName: 'Sprint Retrospective',
    projectName: 'Project Beta',
    formats: [
      { channel: 'Slack', status: 'pending' },
      { channel: 'Mail to Developers', status: 'pending' }
    ]
  }
];

export const mockPlugins: Plugin[] = [
  {
    id: '1',
    type: 'teams',
    profileName: 'Company Teams - Main',
    isActive: true,
    lastSynced: '2025-10-05T08:30:00Z'
  },
  {
    id: '2',
    type: 'teams',
    profileName: 'Company Teams - Dev',
    isActive: true,
    lastSynced: '2025-10-05T08:30:00Z'
  },
  {
    id: '3',
    type: 'outlook',
    profileName: 'work@company.com',
    isActive: true,
    lastSynced: '2025-10-05T07:15:00Z'
  },
  {
    id: '4',
    type: 'slack',
    profileName: 'Engineering Workspace',
    isActive: true,
    lastSynced: '2025-10-05T09:00:00Z'
  }
];
