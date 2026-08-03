import React from 'react';
import { Student, GradeTarget, SchoolSettings } from '../types';
import { ContactCard } from './ContactCard';
import { Users, UserCheck, Heart, Award, Target, School } from 'lucide-react';

interface DashboardProps {
  students: Student[];
  targets: Record<string, GradeTarget>;
  settings: SchoolSettings;
  onNavigate: (tab: string) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({
  students,
  targets,
  settings,
  onNavigate,
}) => {
  // Filter students for current school if set
  const filteredStudents = students.filter(
    (s) => !settings.savedSchoolName || s.manaBarumsaa === settings.savedSchoolName || s.manaBarumsaa === ''
  );

  const totalStudents = filteredStudents.length;
  const maleStudents = filteredStudents.filter((s) => s.koorniyaa === 'Dhiira').length;
  const femaleStudents = filteredStudents.filter((s) => s.koorniyaa === 'Dhalaa').length;
  const disabledStudents = filteredStudents.filter((s) => s.miidhamaQaamaa === 'Eeyyee').length;

  // Grade breakdown
  const gradesList = Array.from({ length: 12 }, (_, i) => String(i + 1));
  const gradeCounts = gradesList.map((g) => {
    const inGrade = filteredStudents.filter((s) => s.kutaa === g);
    const dhiira = inGrade.filter((s) => s.koorniyaa === 'Dhiira').length;
    const dhalaa = inGrade.filter((s) => s.koorniyaa === 'Dhalaa').length;
    const target = targets[g] ? targets[g].dhiira + targets[g].dhalaa : 0;
    return {
      grade: g,
      total: inGrade.length,
      dhiira,
      dhalaa,
      target,
    };
  });

  // Calculate overall target vs actual
  const totalTarget = (Object.values(targets) as GradeTarget[]).reduce((acc, t) => acc + (t.dhiira || 0) + (t.dhalaa || 0), 0);
  const targetPct = totalTarget > 0 ? ((totalStudents / totalTarget) * 100).toFixed(1) : '0';

  return (
    <div className="space-y-6">
      
      {/* Cover / Welcome Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-slate-900 via-indigo-950 to-purple-950 p-8 text-white shadow-2xl border-2 border-amber-400/40">
        <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6 text-center md:text-left">
          <div className="space-y-2 max-w-2xl">
            <span className="inline-block px-3 py-1 bg-amber-400/20 text-amber-300 border border-amber-400/40 text-xs font-bold rounded-full uppercase tracking-widest">
              ✨ Student Management System
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
              Baga Nagaan Dhuftan!
            </h2>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
              Systema Galmee Barattootaa fi Odeeffannoo EMIS - Mana Barumsaa{' '}
              <strong className="text-amber-300 font-semibold">{settings.savedSchoolName}</strong> (Bara{' '}
              {settings.baraBarnootaa})
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
            <button
              onClick={() => onNavigate('students')}
              className="px-6 py-3 bg-gradient-to-r from-amber-400 to-amber-300 hover:from-amber-300 hover:to-amber-200 text-slate-900 font-bold rounded-2xl shadow-lg transition transform hover:-translate-y-0.5 cursor-pointer text-sm"
            >
              ➕ Barataa Haaraa Galmeessi
            </button>
            <button
              onClick={() => onNavigate('reports')}
              className="px-6 py-3 bg-slate-800/80 hover:bg-slate-700 border border-indigo-700/60 text-white font-semibold rounded-2xl transition cursor-pointer text-sm"
            >
              📄 Gabaasa Ilaali
            </button>
          </div>
        </div>
      </div>

      {/* Metric Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Total Students */}
        <div className="bg-white p-6 rounded-2xl border-2 border-slate-200 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Waliigala Barattootaa
            </span>
            <div className="w-10 h-10 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center font-bold">
              <Users className="w-5 h-5" />
            </div>
          </div>
          <h2 className="text-3xl font-extrabold text-blue-600 mb-1">{totalStudents}</h2>
          <p className="text-xs text-slate-500">Total Registered Students</p>
        </div>

        {/* Male Students */}
        <div className="bg-white p-6 rounded-2xl border-2 border-slate-200 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Dhiira (Male)
            </span>
            <div className="w-10 h-10 rounded-xl bg-sky-100 text-sky-600 flex items-center justify-center font-bold">
              <UserCheck className="w-5 h-5" />
            </div>
          </div>
          <h2 className="text-3xl font-extrabold text-sky-600 mb-1">{maleStudents}</h2>
          <p className="text-xs text-slate-500">
            {totalStudents > 0 ? `${((maleStudents / totalStudents) * 100).toFixed(1)}% of total` : '0%'}
          </p>
        </div>

        {/* Female Students */}
        <div className="bg-white p-6 rounded-2xl border-2 border-slate-200 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Dhalaa (Female)
            </span>
            <div className="w-10 h-10 rounded-xl bg-rose-100 text-rose-600 flex items-center justify-center font-bold">
              <Heart className="w-5 h-5" />
            </div>
          </div>
          <h2 className="text-3xl font-extrabold text-rose-600 mb-1">{femaleStudents}</h2>
          <p className="text-xs text-slate-500">
            {totalStudents > 0 ? `${((femaleStudents / totalStudents) * 100).toFixed(1)}% of total` : '0%'}
          </p>
        </div>

        {/* Target Progress */}
        <div className="bg-white p-6 rounded-2xl border-2 border-slate-200 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Raawwii Karooraa
            </span>
            <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold">
              <Target className="w-5 h-5" />
            </div>
          </div>
          <h2 className="text-3xl font-extrabold text-emerald-600 mb-1">{targetPct}%</h2>
          <p className="text-xs text-slate-500">
            Target: {totalTarget} | Actual: {totalStudents}
          </p>
        </div>

      </div>

      {/* Grade Level Summary Table / Visual Progress */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Award className="w-5 h-5 text-indigo-600" />
              <span>Raawwii Kutaa Kutaadhaan (Grade Level Distribution)</span>
            </h3>
            <p className="text-xs text-slate-500">Baay'ina barattoota kutaa 1 - 12</p>
          </div>
          <button
            onClick={() => onNavigate('targets')}
            className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 underline"
          >
            Karoora Jijjiiri →
          </button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {gradeCounts.map((g) => {
            const pct = g.target > 0 ? Math.min(100, Math.round((g.total / g.target) * 100)) : 0;
            return (
              <div
                key={g.grade}
                className="p-4 bg-slate-50 border border-slate-200 rounded-xl hover:border-indigo-300 transition"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-extrabold text-slate-800 text-sm">Kutaa {g.grade}</span>
                  <span className="text-xs font-semibold text-indigo-600">{g.total}</span>
                </div>

                <div className="flex justify-between text-[11px] text-slate-500 mb-2">
                  <span>👨 {g.dhiira}</span>
                  <span>👩 {g.dhalaa}</span>
                </div>

                {/* Progress bar */}
                <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${pct}%` }}
                  />
                </div>
                <div className="text-[10px] text-slate-400 mt-1 text-right font-mono">
                  Target: {g.target} ({pct}%)
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Quick Statistics Banner & Contact Card */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Special Needs & Demographics Card */}
        <div className="lg:col-span-2 bg-gradient-to-br from-indigo-900 to-slate-900 text-white rounded-2xl p-6 shadow-md border border-indigo-800 flex flex-col justify-between">
          <div>
            <span className="text-xs font-bold text-amber-300 uppercase tracking-wider">
              Barattoota Miidhama Qaamaa Qaban
            </span>
            <h3 className="text-xl font-extrabold text-white mt-1 mb-3">
              Special Needs & Inclusion Overview
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 my-4">
              <div className="p-4 bg-indigo-950/70 border border-indigo-700/60 rounded-xl">
                <p className="text-xs text-slate-300">Waliigala Miidhama Qaamaa</p>
                <p className="text-2xl font-bold text-amber-400 mt-1">{disabledStudents} Barattoota</p>
                <p className="text-[11px] text-slate-400 mt-1">
                  {totalStudents > 0 ? `${((disabledStudents / totalStudents) * 100).toFixed(1)}% of all registered` : '0%'}
                </p>
              </div>
              <div className="p-4 bg-indigo-950/70 border border-indigo-700/60 rounded-xl">
                <p className="text-xs text-slate-300">Mana Barumsaa Ammee</p>
                <p className="text-lg font-bold text-white mt-1 truncate" title={settings.savedSchoolName}>
                  {settings.savedSchoolName}
                </p>
                <p className="text-[11px] text-slate-400 mt-1">Bara Barnootaa: {settings.baraBarnootaa}</p>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-indigo-800 flex items-center justify-between text-xs text-slate-300">
            <span className="flex items-center gap-1">
              <School className="w-4 h-4 text-amber-400" /> Systema Galmee Kitesa Negasa Feyisa
            </span>
            <button
              onClick={() => onNavigate('settings')}
              className="text-amber-300 font-semibold hover:underline"
            >
              Qindaa'ina Jijjiiri →
            </button>
          </div>
        </div>

        {/* Author Contact Card */}
        <ContactCard />

      </div>

    </div>
  );
};
