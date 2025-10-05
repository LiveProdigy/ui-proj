import { useState } from 'react';
import { ArrowRight } from 'lucide-react';
import { Meeting } from '../types';
import { mockMeetings } from '../data/mockData';
import MeetingDetail from './MeetingDetail';
import teamsIcon from '../assets/microsoft-teams-svgrepo-com.svg';
import outlookIcon from '../assets/ms-outlook-svgrepo-com.svg';
import gmailIcon from '../assets/gmail-svgrepo-com.svg';
import slackIcon from '../assets/slack-svgrepo-com.svg';

export default function Dashboard() {
  const [selectedMeeting, setSelectedMeeting] = useState<Meeting | null>(null);

  if (selectedMeeting) {
    return (
      <MeetingDetail
        meeting={selectedMeeting}
        onBack={() => setSelectedMeeting(null)}
      />
    );
  }

  const getPlatformIcon = (platform: string) => {
    const icons = {
      teams: teamsIcon,
      zoom: gmailIcon,
      meet: gmailIcon
    };
    return icons[platform as keyof typeof icons] || gmailIcon;
  };

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const [editingField, setEditingField] = useState<{ id: string; field: string } | null>(null);
  const [editedMeetings, setEditedMeetings] = useState(mockMeetings);

  const handleDoubleClick = (id: string, field: string) => {
    setEditingField({ id, field });
  };

  const handleBlur = (id: string, field: string, value: string) => {
    setEditedMeetings(editedMeetings.map(m =>
      m.id === id ? { ...m, [field]: value } : m
    ));
    setEditingField(null);
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">All your recorded meetings in one place</p>
      </div>

      <div className="space-y-6">
        {editedMeetings.map((meeting, index) => (
          <div
            key={meeting.id}
            className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
          >
            <div className="flex flex-col lg:flex-row">
              {/* Video Preview */}
              <div className="lg:w-1/3 bg-gray-900 flex items-center justify-center p-8">
                <div className="w-full aspect-video bg-gray-800 rounded-lg flex items-center justify-center relative group">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-16 h-16 rounded-full bg-white bg-opacity-20 flex items-center justify-center backdrop-blur-sm">
                      <div className="w-0 h-0 border-t-8 border-t-transparent border-l-12 border-l-white border-b-8 border-b-transparent ml-1"></div>
                    </div>
                  </div>
                  <div className="absolute bottom-3 left-3 bg-black bg-opacity-75 px-2 py-1 rounded text-xs text-white">
                    Video {index + 1}
                  </div>
                </div>
              </div>

              {/* Content */}
              <div className="lg:w-2/3 p-6 flex flex-col justify-between">
                <div>
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      {editingField?.id === meeting.id && editingField?.field === 'title' ? (
                        <input
                          type="text"
                          defaultValue={meeting.title}
                          onBlur={(e) => handleBlur(meeting.id, 'title', e.target.value)}
                          autoFocus
                          className="text-xl font-bold text-gray-900 border-b-2 border-blue-500 focus:outline-none w-full"
                        />
                      ) : (
                        <h3
                          className="text-xl font-bold text-gray-900 cursor-text"
                          onDoubleClick={() => handleDoubleClick(meeting.id, 'title')}
                        >
                          {meeting.title}
                        </h3>
                      )}
                      {editingField?.id === meeting.id && editingField?.field === 'description' ? (
                        <textarea
                          defaultValue={meeting.description}
                          onBlur={(e) => handleBlur(meeting.id, 'description', e.target.value)}
                          autoFocus
                          className="text-sm text-gray-600 mt-2 border-b-2 border-blue-500 focus:outline-none w-full resize-none"
                          rows={2}
                        />
                      ) : (
                        <p
                          className="text-sm text-gray-600 mt-2 cursor-text"
                          onDoubleClick={() => handleDoubleClick(meeting.id, 'description')}
                        >
                          {meeting.description}
                        </p>
                      )}
                    </div>
                    <img
                      src={getPlatformIcon(meeting.platform)}
                      alt={meeting.platform}
                      className="w-8 h-8 ml-4"
                    />
                  </div>

                  {/* Client Summary */}
                  <div className="bg-gray-50 rounded-lg p-4 mb-4">
                    <h4 className="text-xs font-semibold text-gray-500 uppercase mb-3">Client Summary</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      <div className="flex items-center gap-2">
                        <img src={teamsIcon} alt="Teams" className="w-5 h-5" />
                        <span className="text-xs text-gray-700">Main</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <img src={teamsIcon} alt="Teams" className="w-5 h-5" />
                        <span className="text-xs text-gray-700">Dev</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <img src={outlookIcon} alt="Outlook" className="w-5 h-5" />
                        <span className="text-xs text-gray-700">Stakeholders</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <img src={slackIcon} alt="Slack" className="w-5 h-5" />
                        <span className="text-xs text-gray-700">Minutes</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* View Details Button */}
                <div className="flex justify-end">
                  <button
                    onClick={() => setSelectedMeeting(meeting)}
                    className="group flex items-center gap-2 bg-blue-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-all hover:gap-3"
                  >
                    <span>View Details</span>
                    <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
