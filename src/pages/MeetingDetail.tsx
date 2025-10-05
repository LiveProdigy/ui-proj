import { useState } from 'react';
import { ArrowLeft, Send, CreditCard as Edit2, ExternalLink } from 'lucide-react';
import { Meeting } from '../types';

interface MeetingDetailProps {
  meeting: Meeting;
  onBack: () => void;
}

export default function MeetingDetail({ meeting, onBack }: MeetingDetailProps) {
  const [activeTab, setActiveTab] = useState<'client' | 'developer' | 'coordinator'>('client');
  const [editMode, setEditMode] = useState(false);
  const [summaries, setSummaries] = useState(meeting.summaries);
  const [notes, setNotes] = useState(meeting.notes);

  const tabs = [
    { id: 'client', label: 'Client Summary' },
    { id: 'developer', label: 'Developer Notes' },
    { id: 'coordinator', label: 'Coordinator Report' }
  ] as const;

  const handleSend = () => {
    alert(`Sending ${activeTab} summary through configured channels...`);
  };

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
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
        <div className="relative h-64 bg-gray-100">
          <img
            src={meeting.thumbnailUrl}
            alt={meeting.title}
            className="w-full h-full object-cover"
          />
        </div>

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

          <div className="bg-gray-50 rounded-lg p-6 mb-6">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                {tabs.find(t => t.id === activeTab)?.label}
              </h3>
              <button
                onClick={() => setEditMode(!editMode)}
                className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
              >
                <Edit2 className="w-4 h-4" />
                <span className="text-sm">{editMode ? 'Save' : 'Edit'}</span>
              </button>
            </div>

            {editMode ? (
              <textarea
                value={summaries[activeTab]}
                onChange={(e) => setSummaries({ ...summaries, [activeTab]: e.target.value })}
                className="w-full h-48 p-4 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            ) : (
              <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                {summaries[activeTab]}
              </div>
            )}

            <div className="mt-6 flex justify-end">
              <button
                onClick={handleSend}
                className="flex items-center gap-2 bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors"
              >
                <Send className="w-4 h-4" />
                <span>Send Report</span>
              </button>
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Meeting Notes</h3>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="w-full h-32 p-4 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Add your meeting notes here..."
              />
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Transcript</h3>
              <div className="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
                <p className="text-gray-700 text-sm whitespace-pre-wrap">{meeting.transcript}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
