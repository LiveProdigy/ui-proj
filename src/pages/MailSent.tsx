import { mockSentCommunications, mockMeetings } from '../data/mockData';
import { CheckCircle2, Clock, Eye } from 'lucide-react';
import { useState } from 'react';

export default function MailSent() {
  const [selectedMeeting, setSelectedMeeting] = useState<string | null>(null);
  const [editingField, setEditingField] = useState<{ id: string; field: string } | null>(null);
  const [communications, setCommunications] = useState(mockSentCommunications);

  const getProgress = (formats: { status: string }[]) => {
    const sent = formats.filter(f => f.status === 'sent').length;
    return { sent, total: formats.length };
  };

  const getProgressColor = (sent: number, total: number) => {
    const percentage = (sent / total) * 100;
    if (percentage === 100) return 'text-green-600';
    if (percentage === 0) return 'text-gray-400';
    return 'text-blue-600';
  };

  const handleDoubleClick = (id: string, field: string) => {
    setEditingField({ id, field });
  };

  const handleBlur = (id: string, field: string, value: string) => {
    setCommunications(communications.map(c =>
      c.meetingId === id ? { ...c, [field]: value } : c
    ));
    setEditingField(null);
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Mail Sent</h1>
        <p className="text-gray-600">Track communication status for all meetings</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Meeting Name</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Project</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Formats</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Progress</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {communications.map((comm) => {
              const progress = getProgress(comm.formats);
              return (
                <tr key={comm.meetingId} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4">
                    {editingField?.id === comm.meetingId && editingField?.field === 'meetingName' ? (
                      <input
                        type="text"
                        defaultValue={comm.meetingName}
                        onBlur={(e) => handleBlur(comm.meetingId, 'meetingName', e.target.value)}
                        autoFocus
                        className="font-medium text-gray-900 border-b-2 border-blue-500 focus:outline-none"
                      />
                    ) : (
                      <div
                        className="font-medium text-gray-900 cursor-text"
                        onDoubleClick={() => handleDoubleClick(comm.meetingId, 'meetingName')}
                      >
                        {comm.meetingName}
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    {editingField?.id === comm.meetingId && editingField?.field === 'projectName' ? (
                      <input
                        type="text"
                        defaultValue={comm.projectName}
                        onBlur={(e) => handleBlur(comm.meetingId, 'projectName', e.target.value)}
                        autoFocus
                        className="text-gray-600 border-b-2 border-blue-500 focus:outline-none"
                      />
                    ) : (
                      <div
                        className="text-gray-600 cursor-text"
                        onDoubleClick={() => handleDoubleClick(comm.meetingId, 'projectName')}
                      >
                        {comm.projectName}
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      {comm.formats.map((format, idx) => (
                        <div key={idx} className="flex items-center gap-2 text-sm">
                          {format.status === 'sent' ? (
                            <CheckCircle2 className="w-4 h-4 text-green-600" />
                          ) : (
                            <Clock className="w-4 h-4 text-gray-400" />
                          )}
                          <span className={format.status === 'sent' ? 'text-gray-900' : 'text-gray-500'}>
                            {format.channel}
                          </span>
                        </div>
                      ))}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="text-sm font-medium">
                        <span className={getProgressColor(progress.sent, progress.total)}>
                          {progress.sent}/{progress.total}
                        </span>
                        <span className="text-gray-500 ml-1">Sent</span>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => setSelectedMeeting(comm.meetingId)}
                      className="flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors"
                    >
                      <Eye className="w-4 h-4" />
                      <span>Open</span>
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
