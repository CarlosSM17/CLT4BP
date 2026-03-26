<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    public function run(): void
    {
        // Admin por defecto
        User::create([
            'name' => 'Admin CLT4BP',
            'email' => 'admin@clt4bp.com',
            'password' => Hash::make('admin123'),
            'role' => 'admin',
            'email_verified_at' => now(),
        ]);

        // Instructor de prueba
        User::create([
            'name' => 'Instructor Demo',
            'email' => 'instructor@clt4bp.com',
            'password' => Hash::make('instructor123'),
            'role' => 'instructor',
            'email_verified_at' => now(),
        ]);

        // Estudiante de prueba
        User::create([
            'name' => 'Estudiante Demo',
            'email' => 'estudiante@clt4bp.com',
            'password' => Hash::make('estudiante123'),
            'role' => 'student',
            'email_verified_at' => now(),
        ]);
    }
}
