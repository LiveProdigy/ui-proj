import { useState } from 'react';
import { ArrowLeft, Send, ExternalLink } from 'lucide-react';
import { Meeting } from '../types';
import teamsIcon from '../assets/microsoft-teams-svgrepo-com.svg';
import outlookIcon from '../assets/ms-outlook-svgrepo-com.svg';
import slackIcon from '../assets/slack-svgrepo-com.svg';

interface MeetingDetailProps {
  meeting: Meeting;
  onBack: () => void;
}

interface DeveloperNote {
  timestamp: string;
  duration: string;
  speaker: string;
  content: string;
}

interface CoordinatorChannel {
  icon: string;
  name: string;
  content: string;
  recipientLabel: string;
  recipients: string[];
}

export default function MeetingDetail({ meeting, onBack }: MeetingDetailProps) {
  const [activeTab, setActiveTab] = useState<'client' | 'developer' | 'coordinator'>('client');
  const [editingField, setEditingField] = useState<string | null>(null);

  const [clientSummary, setClientSummary] = useState(meeting.summaries.client);
  const [notes, setNotes] = useState(meeting.notes);
  const [transcript, setTranscript] = useState(meeting.transcript);

  const [developerNotes, setDeveloperNotes] = useState<DeveloperNote[]>([
    { timestamp: '1:00 - 1:25', duration: '25s', speaker: 'John Smith', content: 'Discussed API integration requirements and authentication flow' },
    { timestamp: '1:25 - 2:10', duration: '45s', speaker: 'Sarah Johnson', content: 'Reviewed database schema changes needed for new features' },
    { timestamp: '2:10 - 3:05', duration: '55s', speaker: 'Mike Chen', content: 'Outlined frontend component architecture and state management' },
    { timestamp: '3:05 - 4:00', duration: '55s', speaker: 'John Smith', content: 'Action items: Complete API docs by Friday, setup staging environment' }
  ]);

  const [coordinatorChannels, setCoordinatorChannels] = useState<CoordinatorChannel[]>([
    {
      icon: teamsIcon,
      name: 'Teams - Main',
      content: 'Quarterly planning completed successfully. All stakeholders aligned on Q1 priorities and timeline. Next meeting scheduled for feature review.',
      recipientLabel: 'Channel',
      recipients: ['@general', 'Sarah Johnson', 'Mike Chen', 'Lisa Wong']
    },
    {
      icon: teamsIcon,
      name: 'Teams - Dev',
      content: 'Technical requirements finalized. API integration approved. Database migration planned for next sprint. Code review scheduled for Monday.',
      recipientLabel: 'Group',
      recipients: ['@developers', 'John Smith', 'Alex Kumar', 'Emma Davis']
    },
    {
      icon: outlookIcon,
      name: 'Stakeholders',
      content: 'Meeting summary: Product roadmap for Q1 confirmed. Key deliverables include API v2.0, enhanced dashboard, and mobile optimization. Timeline approved by leadership team.',
      recipientLabel: 'Mail to',
      recipients: ['ceo@company.com', 'cto@company.com', 'product-leads@company.com']
    },
    {
      icon: slackIcon,
      name: 'Meeting of Minutes',
      content: 'Action items: 1) API documentation - John (Due: Friday) 2) Design mockups - Sarah (Due: Wednesday) 3) Database schema - Mike (Due: Thursday) 4) Sprint planning - Team (Due: Next Monday)',
      recipientLabel: 'Members to deliver',
      recipients: ['#project-updates', 'John Smith', 'Sarah Johnson', 'Mike Chen']
    }
  ]);

  const tabs = [
    { id: 'client', label: 'Client Summary' },
    { id: 'developer', label: 'Developer Notes' },
    { id: 'coordinator', label: 'Coordinator Report' }
  ] as const;

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleDoubleClick = (field: string) => {
    setEditingField(field);
  };

  const handleBlur = (field: string, value: string) => {
    if (field === 'clientSummary') setClientSummary(value);
    if (field === 'notes') setNotes(value);
    if (field === 'transcript') setTranscript(value);
    setEditingField(null);
  };

  const updateDeveloperNote = (index: number, field: keyof DeveloperNote, value: string) => {
    const updated = [...developerNotes];
    updated[index] = { ...updated[index], [field]: value };
    setDeveloperNotes(updated);
  };

  const updateCoordinatorChannel = (index: number, field: 'content', value: string) => {
    const updated = [...coordinatorChannels];
    updated[index] = { ...updated[index], [field]: value };
    setCoordinatorChannels(updated);
  };

  return (
    <div className="p-8">
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6 transition-colors"
      >
        <ArrowLeft className="w-5 h-5" />
        <span className="font-medium">Back to Dashboard</span>
      </button>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="p-8">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{meeting.title}</h1>
            <p className="text-gray-600 mb-4">{meeting.description}</p>
            <div className="flex items-center gap-6 text-sm text-gray-500">
              <span>{formatDate(meeting.meetingDate)}</span>
              <span className="capitalize">{meeting.platform}</span>
              {meeting.externalLink && (
                <a
                  href={meeting.externalLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 text-blue-600 hover:text-blue-700"
                >
                  <ExternalLink className="w-4 h-4" />
                  <span>View in Read AI</span>
                </a>
              )}
            </div>
          </div>

          <div className="border-b border-gray-200 mb-6">
            <div className="flex gap-1">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-6 py-3 font-medium transition-colors relative ${
                    activeTab === tab.id
                      ? 'text-blue-600'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {tab.label}
                  {activeTab === tab.id && (
                    <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600"></div>
                  )}
                </button>
              ))}
            </div>
          </div>

          {activeTab === 'client' && (
            <div>
              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Client Summary</h3>
                  <button className="text-sm text-gray-600 hover:text-gray-900 flex items-center gap-1">
                    <span>Edit</span>
                  </button>
                </div>

                {editingField === 'clientSummary' ? (
                  <textarea
                    defaultValue={clientSummary}
                    onBlur={(e) => handleBlur('clientSummary', e.target.value)}
                    autoFocus
                    className="w-full h-32 p-4 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                ) : (
                  <p
                    className="text-gray-700 cursor-text"
                    onDoubleClick={() => handleDoubleClick('clientSummary')}
                  >
                    {clientSummary}
                  </p>
                )}

                <div className="mt-6 flex justify-end">
                  <button className="flex items-center gap-2 bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors">
                    <Send className="w-4 h-4" />
                    <span>Send Report</span>
                  </button>
                </div>
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Meeting Notes</h3>
                  {editingField === 'notes' ? (
                    <textarea
                      defaultValue={notes}
                      onBlur={(e) => handleBlur('notes', e.target.value)}
                      autoFocus
                      className="w-full h-32 p-4 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <div
                      className="bg-gray-50 rounded-lg p-4 cursor-text text-gray-700"
                      onDoubleClick={() => handleDoubleClick('notes')}
                    >
                      {notes}
                    </div>
                  )}
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Transcript</h3>
                  {editingField === 'transcript' ? (
                    <textarea
                      defaultValue={transcript}
                      onBlur={(e) => handleBlur('transcript', e.target.value)}
                      autoFocus
                      className="w-full h-48 p-4 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <div
                      className="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto cursor-text"
                      onDoubleClick={() => handleDoubleClick('transcript')}
                    >
                      <p className="text-gray-700 text-sm whitespace-pre-wrap">{transcript}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'developer' && (
            <div>
              <div className="space-y-3">
                {developerNotes.map((note, index) => (
                  <div key={index} className="bg-gray-50 rounded-lg p-4">
                    <div className="flex items-start gap-4">
                      <div className="flex items-center gap-2 min-w-fit">
                        {editingField === `dev-time-${index}` ? (
                          <input
                            type="text"
                            defaultValue={note.timestamp}
                            onBlur={(e) => {
                              updateDeveloperNote(index, 'timestamp', e.target.value);
                              setEditingField(null);
                            }}
                            autoFocus
                            className="w-28 px-2 py-1 text-sm border border-blue-500 rounded focus:outline-none"
                          />
                        ) : (
                          <span
                            className="text-sm text-orange-600 font-medium cursor-text"
                            onDoubleClick={() => handleDoubleClick(`dev-time-${index}`)}
                          >
                            {note.timestamp}
                          </span>
                        )}
                        {editingField === `dev-duration-${index}` ? (
                          <input
                            type="text"
                            defaultValue={note.duration}
                            onBlur={(e) => {
                              updateDeveloperNote(index, 'duration', e.target.value);
                              setEditingField(null);
                            }}
                            autoFocus
                            className="w-16 px-2 py-1 text-xs border border-blue-500 rounded focus:outline-none"
                          />
                        ) : (
                          <span
                            className="text-xs text-orange-600 cursor-text"
                            onDoubleClick={() => handleDoubleClick(`dev-duration-${index}`)}
                          >
                            ({note.duration})
                          </span>
                        )}
                      </div>

                      <div className="flex-1">
                        <div className="mb-2">
                          {editingField === `dev-speaker-${index}` ? (
                            <input
                              type="text"
                              defaultValue={note.speaker}
                              onBlur={(e) => {
                                updateDeveloperNote(index, 'speaker', e.target.value);
                                setEditingField(null);
                              }}
                              autoFocus
                              className="px-2 py-1 text-sm font-medium border border-blue-500 rounded focus:outline-none"
                            />
                          ) : (
                            <span
                              className="text-sm font-medium text-blue-600 cursor-text"
                              onDoubleClick={() => handleDoubleClick(`dev-speaker-${index}`)}
                            >
                              {note.speaker}
                            </span>
                          )}
                        </div>
                        {editingField === `dev-content-${index}` ? (
                          <textarea
                            defaultValue={note.content}
                            onBlur={(e) => {
                              updateDeveloperNote(index, 'content', e.target.value);
                              setEditingField(null);
                            }}
                            autoFocus
                            className="w-full p-2 text-sm border border-blue-500 rounded focus:outline-none resize-none"
                            rows={2}
                          />
                        ) : (
                          <p
                            className="text-sm text-gray-700 cursor-text"
                            onDoubleClick={() => handleDoubleClick(`dev-content-${index}`)}
                          >
                            {note.content}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'coordinator' && (
            <div className="space-y-6">
              {coordinatorChannels.map((channel, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-6">
                  <div className="flex items-start gap-4 mb-4">
                    <img src={channel.icon} alt={channel.name} className="w-8 h-8" />
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-900 mb-3">{channel.name}</h4>

                      {editingField === `coord-content-${index}` ? (
                        <textarea
                          defaultValue={channel.content}
                          onBlur={(e) => {
                            updateCoordinatorChannel(index, 'content', e.target.value);
                            setEditingField(null);
                          }}
                          autoFocus
                          className="w-full p-3 text-sm border border-blue-500 rounded-lg focus:outline-none resize-none"
                          rows={3}
                        />
                      ) : (
                        <p
                          className="text-gray-700 text-sm mb-4 cursor-text"
                          onDoubleClick={() => handleDoubleClick(`coord-content-${index}`)}
                        >
                          {channel.content}
                        </p>
                      )}

                      <div>
                        <p className="text-xs font-medium text-gray-600 mb-2">{channel.recipientLabel}:</p>
                        <div className="flex flex-wrap gap-2">
                          {channel.recipients.map((recipient, idx) => (
                            <span
                              key={idx}
                              className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-xs"
                            >
                              {recipient}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
