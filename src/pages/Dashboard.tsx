import { useState } from 'react';
import { Calendar, Video, ExternalLink } from 'lucide-react';
import { Meeting } from '../types';
import { mockMeetings } from '../data/mockData';
import MeetingDetail from './MeetingDetail';

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
      teams: '👥',
      zoom: '🎥',
      meet: '📹'
    };
    return icons[platform as keyof typeof icons] || '📹';
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

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">All your recorded meetings in one place</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockMeetings.map((meeting) => (
          <div
            key={meeting.id}
            className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow"
          >
            <div className="relative h-48 bg-gray-100 overflow-hidden">
              <img
                src={meeting.thumbnailUrl}
                alt={meeting.title}
                className="w-full h-full object-cover"
              />
              <div className="absolute top-3 right-3 bg-white px-2 py-1 rounded-md text-sm font-medium flex items-center gap-1">
                <span>{getPlatformIcon(meeting.platform)}</span>
                <span className="capitalize">{meeting.platform}</span>
              </div>
            </div>

            <div className="p-5">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {meeting.title}
              </h3>
              <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                {meeting.description}
              </p>

              <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                <div className="flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  <span>{formatDate(meeting.meetingDate)}</span>
                </div>
              </div>

              <button
                onClick={() => setSelectedMeeting(meeting)}
                className="w-full bg-blue-600 text-white py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors"
              >
                View Details
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
