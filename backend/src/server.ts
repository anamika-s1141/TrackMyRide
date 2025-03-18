require('dotenv').config();

import express  from "express";
import cors from "cors";

import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";
import type { Request, Response } from "express";

const app = express();
const prisma = new PrismaClient();

app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;

// Test route
app.get("/", (req: Request, res: Response) => {
    console.log(req.method);
    res.json({ msg: "Router works" });
});

// Signup Route
app.post("/signup", async (req: Request, res: Response) => {
    try {
        const { email, password , name} = req.body;

        // Check if user exists
        const existingUser = await prisma.user.findUnique({ where: { email } });
        if (existingUser) {
            return res.status(400).json({ error: "User already exists" });
        }

        // Hash password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create user
        const user = await prisma.user.create({
            data: { email, password: hashedPassword, name },
        });

        res.status(201).json({ msg: "User created successfully", user });
    } catch (error) {
        console.log(error)
        res.status(500).json({ error: "Something went wrong" });
    }
});

// Login Route
app.post("/login", async (req: Request, res: Response) => {
    try {
        const { email, password } = req.body;

        // Find user
        const user = await prisma.user.findUnique({ where: { email } });
        if (!user) {
            return res.status(400).json({ error: "Invalid credentials" });
        }

        // Compare password
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).json({ error: "Invalid credentials" });
        }

        res.status(200).json({ msg: "Login successful", user });
    } catch (error) {
        res.status(500).json({ error: "Something went wrong" });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Server started at: ${PORT}`);
});